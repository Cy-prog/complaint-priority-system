from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Complaint, ComplaintAnalysis, Category

# High-precision municipal anchor coordinates for Gwalior Municipal Corporation (GMC)
GWALIOR_MUNICIPAL_HUBS = {
    "18": {"name": "महाराज बाड़ा / सराफा / लश्कर", "lat": 26.2045, "lng": 78.1578},
    "12": {"name": "हजीरा / किला गेट / तानसेन नगर", "lat": 26.2350, "lng": 78.1760},
    "34": {"name": "थाटीपुर / मयूर मार्केट / गांधी रोड", "lat": 26.2230, "lng": 78.2180},
    "48": {"name": "सिटी सेंटर / कलेक्ट्रेट / बाल भवन", "lat": 26.2025, "lng": 78.1925},
    "22": {"name": "लश्कर / कंपू / माधव डिस्पेंसरी", "lat": 26.1950, "lng": 78.1500},
    "7": {"name": "मुरार सदर बाजार / एमएच चौराहा", "lat": 26.2285, "lng": 78.2290},
    "15": {"name": "फूलबाग / पड़ाव / रेलवे स्टेशन", "lat": 26.2160, "lng": 78.1780},
    "28": {"name": "दीनदयाल नगर / एयरपोर्ट रोड", "lat": 26.2550, "lng": 78.2250},
    "31": {"name": "गोविंदपुरी / जीवाजी विश्वविद्यालय", "lat": 26.2085, "lng": 78.2050},
    "42": {"name": "शिंदे की छावनी / नदी गेट", "lat": 26.2120, "lng": 78.1650},
    "54": {"name": "पिंटो पार्क / मुरार कैंट", "lat": 26.2410, "lng": 78.2380},
    "60": {"name": "आनंद नगर / बहोड़ापुर / मोतीझील", "lat": 26.2450, "lng": 78.1520}
}

DEFAULT_MUNICIPAL_CENTER = (26.2183, 78.1828)  # Gwalior Central HQ

class GISService:
    def get_map_markers(
        self,
        db: Session,
        category_id: int | None = None,
        priority: str | None = None,
        ward: str | None = None,
        limit: int = 300
    ) -> list[dict]:
        """
        Retrieves real GIS spatial coordinates for complaints.
        Uses verified GPS coordinates when available; otherwise looks up exact ward centroid.
        """
        query = db.query(Complaint).order_by(Complaint.created_at.desc())

        if category_id:
            query = query.filter(Complaint.category_id == category_id)
        if ward:
            query = query.filter(Complaint.ward.ilike(f"%{ward}%"))

        complaints = query.limit(limit).all()
        points = []

        for c in complaints:
            prio = c.analysis.priority if c.analysis else "LOW"
            if priority and priority != "ALL" and prio != priority:
                continue

            lat = c.latitude
            lng = c.longitude
            coord_source = "ACCURATE_GPS"

            # If complaint has no direct GPS coordinates, look up exact municipal hub
            if not lat or not lng:
                hub = self._resolve_ward_hub(c.ward, c.area, c.complaint_text)
                if hub:
                    lat, lng = hub["lat"], hub["lng"]
                    coord_source = "WARD_CENTROID"
                else:
                    lat, lng = DEFAULT_MUNICIPAL_CENTER
                    coord_source = "MUNICIPAL_HQ"

            points.append({
                "id": c.complaint_id,
                "lat": round(float(lat), 6),
                "lng": round(float(lng), 6),
                "coord_source": coord_source,
                "title": c.complaint_text[:70] + "..." if len(c.complaint_text) > 70 else c.complaint_text,
                "category": c.category.name if c.category else "Civic Service",
                "priority": prio,
                "status": c.status,
                "ward": c.ward or "General Area",
                "area": c.area or "",
                "photo": c.evidence_photo,
                "resolution_photo": c.resolution_photo,
                "date": c.created_at.strftime("%d-%m-%Y") if c.created_at else "",
                "is_critical": prio == "CRITICAL"
            })

        return points

    def get_ward_spatial_summary(self, db: Session) -> list[dict]:
        """Ward-by-ward spatial aggregation for heatmaps and risk clustering."""
        results = db.query(
            Complaint.ward,
            func.count(Complaint.id).label("total_complaints")
        ).filter(Complaint.ward != None).group_by(Complaint.ward).all()

        ward_stats = []
        for w, tot in results:
            hub = self._resolve_ward_hub(w)
            crit_count = db.query(Complaint).join(ComplaintAnalysis).filter(
                Complaint.ward == w,
                ComplaintAnalysis.priority == "CRITICAL"
            ).count()

            ward_stats.append({
                "ward": w,
                "total_complaints": tot,
                "critical_count": crit_count,
                "lat": hub["lat"] if hub else DEFAULT_MUNICIPAL_CENTER[0],
                "lng": hub["lng"] if hub else DEFAULT_MUNICIPAL_CENTER[1],
                "risk_tier": "VERY_HIGH" if crit_count >= 3 else ("HIGH" if crit_count >= 1 else "NORMAL")
            })

        return sorted(ward_stats, key=lambda x: x["critical_count"], reverse=True)

    def _resolve_ward_hub(self, ward: str | None, area: str | None = None, text: str | None = None) -> dict | None:
        full_str = f"{ward or ''} {area or ''} {text or ''}"
        
        # Match ward number
        import re
        ward_nums = re.findall(r'(\d+)', ward or '')
        for num in ward_nums:
            if num in GWALIOR_MUNICIPAL_HUBS:
                return GWALIOR_MUNICIPAL_HUBS[num]

        # Match locality keyword
        for num, data in GWALIOR_MUNICIPAL_HUBS.items():
            keywords = data["name"].split(" / ")
            for kw in keywords:
                if kw in full_str:
                    return data
        return None
