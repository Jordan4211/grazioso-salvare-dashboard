# Grazioso Salvare Rescue Dog Dashboard


### 1. How do you write programs that are maintainable, readable, and adaptable?

For this project I focused on writing code that was easy to read and reusable instead of having everything hard-coded in one notebook. The main example of this is the `AnimalShelter` class in the CRUD Python module. That class handles all the database work against MongoDB.

There are a few advantages to organizing it this way:

- **Reusability:**  
  The same CRUD module from Project One could be imported directly into the Project Two dashboard. I didn’t need to rewrite database logic for each visualization or callback.

- **Easy to maintain:**  
  If the database connection info, credentials, or collection name changes, it only needs to be updated in one location (the class), not in every part of the app.

- **Clarity:**  
  Each method in the class does one job:
  - `create()` inserts documents
  - `read()` queries and returns results
  - `update()` modifies documents
  - `delete()` removes documents  
  This makes it alot easier to read and potentially debug in the future.

- **Adaptability:**  
  The dashboard used functions like `fetch_df()` and `build_query()` on top of the CRUD module.  
  - `fetch_df()` runs a query, converts results into a Pandas DataFrame, and cleans it for display (like dropping Mongo `_id` objects that would break the table).
  - `build_query()` turns the business rules for each “rescue type” (Water Rescue, Mountain/Wilderness, Disaster/Individual Track) into a MongoDB filter.

Because those rules are in `build_query()`, if Grazioso Salvare changes their criteria, for example, adds new breeds for Mountain Rescue, I only update that one function. The rest of the dashboard (table, charts, map) will use the new logic automatically.

In the future this CRUD module can be reused outside Dash. For example:
- A command-line report generator.
- A daily summary script (email or Slack bot).


### 2. How do you approach a problem as a computer scientist?

My approach was roughly: clarify → design → build → test.

**Clarify the real requirement**  
Grazioso Salvare wasn’t just asking for a database or a chart. They specifically wanted to identify dogs that are good candidates for different types of rescue work. Each rescue type had rules:
- Breed preferences
- Age range (in weeks)
- Preferred sex (e.g. “Intact Male”)
- Dogs only (not cats, etc.)

Those rules told me what kinds of queries I actually needed to support.

**Design with structure (think MVC)**  
I treated the system like a basic MVC(Model, View, Controller) style setup:
- **Model:** MongoDB + the CRUD module (`AnimalShelter`), which knows how to talk to the database.
- **View:** The Dash/JupyterDash UI, radio buttons, interactive data table, donut chart of outcome types, and the map.
- **Controller:** The Dash callbacks and helper functions (`build_query()`, etc.) that take user input (like “Water Rescue”) and run the correct database query, then feed that data into the view.

This separation made it easier. The dashboard doesn’t “think” about MongoDB directly. It just asks for data.

**Build iteratively**  
I built and tested in layers:
1. Import shelter data into MongoDB with `mongoimport`.
2. Write and verify CRUD in isolation (Project One).
3. Display all animals in the dashboard table.
4. Add filter controls (radio buttons for rescue type).
5. Connect those controls to live MongoDB queries.
6. Add visuals (donut chart) and geo map.
7. Make sure interactions update live:
   - Changing the rescue type updates the table rows.
   - The pie chart redraws based on that filtered dataset.
   - The map marker updates to show the selected animal’s location.

This assignment forced me to care about usability like a real client project, not just correctness.

**Test realistically**  
I tested each filter state:
- Reset (all dogs)
- Water Rescue
- Mountain / Wilderness
- Disaster / Individual Track

For each one I checked:
- The data table only showed the intended dogs.
- The donut chart of outcome types updated.
- The Leaflet map pointed to the selected row’s coordinates around Austin.

Going forward I would use this same process for other clients:
1. Translate their business rules into queryable conditions.
2. Wrap data access in a reusable module.
3. Build an interface that reacts to those queries in real time.


### 3. What do computer scientists do, and why does it matter?

Computer scientists build systems that let organizations make better and faster decisions using their data.

In this project the organization is a rescue training company. They need to find dogs that are strong matches for specific rescue roles like water rescue, wilderness search, disaster response, and tracking. Doing that work manually by reading shelter logs would take hours.

This dashboard helps them:

- **Find qualified candidates quickly:**  
  With one click, staff can filter the data set down to only dogs that match a rescue profile. That includes breed groups, age range, and sex.

- **See availability patterns:**  
  The donut chart shows outcome types (Adoption, Transfer, Return to Owner, etc.) for just the filtered dogs. That helps answer questions like, “Do we have a lot of available candidates in this category, or are they mostly already adopted?”

- **Plan logistics:**  
  The map displays the location of the selected animal using latitude/longitude stored in the dataset. Staff can immediately see where the dog is in the Austin area, which helps with transport and training planning.

- **Repeat the process as new data comes in:**  
  Because the dashboard queries MongoDB directly and uses a consistent CRUD layer, it’s not a one-time report. Whenever the shelter data updates, the dashboard can immediately reflect the new candidates.
