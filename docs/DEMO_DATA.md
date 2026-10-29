# Demonstration scenario

The application starts with an empty report table. Use synthetic values below to demonstrate matching without inserting sample data automatically into a shared database.

1. Set a strong initial administrator password in `.env` and start the application.
2. Register an ordinary account and create a LOST report:
   - Title: Black leather wallet
   - Category: Accessories
   - Description: Black leather wallet with brass snap and two card slots
   - Location: Main Library, first floor
   - Date: 2026-09-20
   - Approximate time: 10:00
3. Register a second ordinary account and create a FOUND report:
   - Title: Wallet found near reading tables
   - Category: Accessories
   - Description: Small black leather wallet with brass snap
   - Location: Main Library, first floor
   - Date: 2026-09-20
   - Approximate time: 10:15
4. Sign in to the first account and inspect the notification and component explanation.
5. Sign in as the lost-report owner, review the suggested found item, and submit owner-only proof details if it is yours.
6. Sign in with the configured administrator, review the claimant's proof, then approve or reject the claim. An approval resolves both reports; a rejection keeps them open and the claimant can submit more evidence.

The descriptions and people above are fictional. The close date, time, category, and location make this a predictable demonstration fixture. The score is not a guarantee of ownership.
