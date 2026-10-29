# REST API

The application uses the same Spring Security session as its web interface. Authenticated routes require a valid session; browser POST requests use Spring Security CSRF protection.

| Method | Path | Access | Purpose |
|---|---|---|---|
| GET | `/api/health` | public | process health response |
| GET | `/api/reports?q=&type=` | authenticated | search open reports; type is LOST or FOUND |
| POST | `/api/reports` | authenticated | submit a validated report |
| GET | `/api/reports/{id}` | authenticated | read a report |
| GET | `/api/matches/mine` | authenticated | list matches involving the current user's reports |
| GET | `/api/notifications/mine` | authenticated | latest notifications for the current user |
| POST | `/api/notifications/{id}/read` | authenticated | mark the current user's notification as read |

POST body example:

```json
{"type":"LOST","title":"Navy water bottle","category":"Drinkware","description":"Matte navy bottle with a silver loop","location":"Engineering Library","itemDate":"2026-09-20","itemTime":"10:30:00"}
```

Validation errors return HTTP 400 with an `error` string and a `fields` array. The web interface provides account registration and form-based sign-in. Admin review pages require the ADMIN role.
