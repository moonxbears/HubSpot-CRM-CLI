import os
import sys
import hubspot.crm


# {
#     "paging": {"next": {"after": "10", "link": None}},
#     "results": [
#         {
#             "archived": False,
#             "archived_at": None,
#             "created_at": datetime.datetime(
#                 2025, 2, 24, 22, 7, 4, 383000, tzinfo=tzutc()
#             ),
#             "id": "89150940859",
#             "properties": {
#                 "createdate": "2025-02-24T22:07:04.383Z",
#                 "email": "emailmaria@hubspot.com",
#                 "firstname": "Maria",
#                 "hs_object_id": "89150940859",
#                 "lastmodifieddate": "2025-03-06T19:33:33.618Z",
#                 "lastname": "Johnson (Sample Contact)",
#             },
#             "properties_with_history": None,
#             "updated_at": datetime.datetime(
#                 2025, 3, 6, 19, 33, 33, 618000, tzinfo=tzutc()
#             ),
#         }
#     ],
#     "total": 120,
# }