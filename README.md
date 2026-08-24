# Liya's World — README

A private family keepsake and third-grade learning portal built for Liya (2026–2027, 3rd grade). This document explains how to run it, how to update it week to week, and how the data works.

## What's in this folder

```
index.html              The whole app shell (loads everything below)
css/
  styles.css             All styling — colors, layout, components
js/
  storage.js             Reads/writes localStorage; export/import/backup
  app.js                 Navigation, routing, Liya/Parent mode, search
  learning.js             Learning Center: subjects, lessons, practice, quizzes tab
  quizzes.js             The quiz-taking engine
  homework.js             Homework Center + Today's Learning
  reading.js              Reading Center
  keepsake.js              Creations, Achievements, Memories, Dreams, Growth, Messages, Guestbook
  parent-dashboard.js     Parent Dashboard: overview, weekly plan editor, test scores, settings
data/
  subjects.js             All 11 subjects' units & lessons (the actual curriculum content)
  curriculum.js           Quizzes, math-practice generators, Amharic vocab, 12-week program, settings
img/
  liya-hero.jpg           Her photo (reused site-wide)
liyas-world-bundled.html  A single-file version of the same app (see "Publishing" below)
build_bundle.py           The script that generates the bundled file, if you ever need to regenerate it
```

## 1. Running it locally

Because the app loads its JavaScript files with plain `<script src="...">` tags (not ES modules), you can simply **double-click `index.html`** and it will open and run in your browser, no server required. This works in Chrome, Safari, Firefox, and Edge.

If double-clicking ever behaves oddly in your browser (some browsers are stricter about local files), run a tiny local server instead from this folder and open the printed address:

```bash
# Python (usually already installed on Mac):
python3 -m http.server 8080
# then open http://localhost:8080/index.html

# or Node, if you have it:
npx serve .
```

## 2. Deploying it online (optional)

This is a fully static site — no backend, no build step. Any static host works:

- **Simplest / free:** drag the whole folder into [Netlify Drop](https://app.netlify.com/drop), or connect the folder to Vercel or GitHub Pages.
- Keep the `<meta name="robots" content="noindex, nofollow">` tag in `index.html` — it asks search engines not to index the page — but understand that **this does not make the page private**. Anyone who has (or guesses, or finds in server logs, browser history, a shared link, etc.) the exact URL can open it. If you deploy this online:
  - Use your host's password-protection feature if it has one (Netlify Pro, Vercel password protection, etc.), or
  - Put it behind your home network / a private VPN, or
  - Just keep it local on your own computer(s), which is the default and simplest option.
- The in-app "Parent Mode PIN" (default `0000`, changeable in Parent → Settings) is a **convenience lock for a young child casually clicking around, not real security.** Anyone who opens the browser's developer tools can bypass it instantly. Don't put anything in this app you wouldn't want visible to anyone with the URL.

## 3. How data storage works

Every bit of parent-entered information (homework, reading log, achievements, quiz results, notes, weekly plans, settings) lives in your browser's **`localStorage`**, scoped to this one file/URL, on this one device, in this one browser.

**What that means in practice:**
- Refreshing the page is safe — your data stays.
- Opening the site in a different browser (or a different computer, or a private/incognito window) starts fresh — it does *not* see data entered elsewhere. There is no automatic sync between devices.
- Clearing your browser's site data/cookies for this page will erase it.
- Nothing is ever sent to a server. This is genuinely private by architecture, not just by policy — there's no network request carrying Liya's information anywhere (the only external request the page makes at all is loading the Google Fonts stylesheet).

**Because of the above, back up regularly** — see the next section.

## 4. Updating homework every week (no code required)

1. Switch to **Parent Mode** (top-right toggle, PIN `0000` by default).
2. Go to **Homework**.
3. Click **+ Add Homework**, fill in subject/title/instructions/due date/priority/etc., and click **Save**. It appears immediately in both the Homework Center and, if due today, in Liya's **Today** view.
4. To reuse the family's usual weekly rhythm (reading every weekday, Amharic on Monday, Ethiopia on Tuesday, Orthodox formation Saturday, church Sunday, etc.), click **Use Weekly Template** on the Homework page — it fills in that week's family-learning items automatically. You can still edit or delete any of them afterward.
5. Use **← Previous Week / Next Week →** to navigate; homework is grouped by due date automatically, so there's no separate "create a new week" step — just add homework with the due date you want and it lands in the right week.
6. Update **This Week's** learning-plan focus areas and your private Parent Notes from **Parent → This Week**.

Editing and deleting both homework and books/achievements/memories work the same way everywhere in Parent Mode: look for the pencil (✏️) and trash (🗑️) icons, or the **Edit/Delete** buttons on each card.

## 5. Adding or changing curriculum content

The lessons themselves (11 subjects × real 3rd-grade lessons) live in **`data/subjects.js`** as plain JavaScript objects — there's no in-app editor for lesson content by design, since it's meant to be a stable curriculum you occasionally extend, not something edited casually from a phone.

To add a new lesson, open `data/subjects.js` in any text editor and copy an existing lesson object inside the subject/unit you want, then edit the text fields (`title`, `objective`, `explain`, `example`, `guidedPractice`, `independentPractice`, `vocab`, `review`, `activity`, `parentQuestions`, `homeworkSuggestion`, `checkpoint`). Give it a unique `id` (e.g. `math-l8`). Save the file and refresh the page — it appears automatically in the Learning Center, complete with progress tracking.

Quizzes live in `data/curriculum.js` under `QUIZZES`, keyed by an id you can reference from a lesson's optional `quizId` field. Amharic vocabulary lives in the same file under `AMHARIC_VOCAB`. The 12-week program outline (used for "Program Week N" labeling) is under `PROGRAM_WEEKS` — weeks 13+ don't need any code change, they're computed automatically from the program start date in Settings.

## 6. Backing up your data

Go to **Parent → Settings & Data → Export Backup (.json)**. This downloads everything you've entered as one JSON file. Do this:
- Right after a session where you added a lot (a new week, several achievements, etc.)
- Before clearing your browser's data
- Before switching to a new computer or browser
- Periodically, just as good practice (monthly is plenty)

To restore, go to the same Settings tab, choose the file with **Import Backup**, and pick **Merge** (adds/updates without removing anything currently on this device) or **Replace** (wipes current data and restores exactly what's in the file). Corrupted or invalid files are rejected with a clear message — they won't silently damage your existing data.

## 7. Publishing / the bundled single-file version

`liyas-world-bundled.html` is the exact same application as everything above, generated by `build_bundle.py`, with all CSS/JS inlined and the photo embedded — a single file with no other files needed. It behaves identically (same localStorage-based data, same everything) and is what gets used if this is published as a hosted, private link. If you ever edit the source files and want to regenerate it, run:

```bash
python3 build_bundle.py
```

## 8. Migrating to a real backend later

If down the road you want the data to sync across devices (e.g., both parents' phones, or Liya's own tablet), a static `localStorage`-only site can't do that — `localStorage` is inherently per-browser. The cleanest path, without a rewrite:

1. **Keep the front-end as-is.** Every place the app touches data goes through the small set of functions in `js/storage.js` (`getData`, `updateData`, `exportDataToFile`, `importDataFromFile`) — that's intentional, so this is the *only* file that would need to change.
2. **Add a backend** — [Supabase](https://supabase.com) or [Firebase](https://firebase.google.com) are the fastest realistic options for a project this size: both give you a hosted database, a JS SDK, and real authentication (actual accounts + passwords, not a front-end PIN) with a generous free tier.
3. **Swap the storage functions:** `getData()` would `fetch`/query the backend instead of reading `localStorage`; `updateData()` would write to it (optimistically updating the UI, then syncing). The exported JSON schema in this app (one object with `homework`, `readingLog`, `achievements`, `weeks`, `quizResults`, etc.) maps cleanly onto either a single JSON-column document per family or a few normalized tables, if you'd rather go that route.
4. **Add real authentication** (Supabase Auth / Firebase Auth — email+password or a magic link) so "Parent Mode" becomes an actual login instead of a convenience PIN, and each family's data is genuinely private and access-controlled server-side.
5. Everything else — the Learning Center content, the UI, the quiz engine, the whole design — needs no changes at all.

## 9. Privacy notes

- No analytics, tracking scripts, or third-party API calls of any kind. The only external network request the page makes is the Google Fonts stylesheet.
- No school name, address, or other identifying details are stored anywhere by default — the demo/seed data deliberately keeps things general. If you type such details into a note field yourself, they're stored the same way as everything else (locally, per the explanation above) — nothing is transmitted anywhere, but do keep in mind the PIN is not real security if you ever put this behind a public URL.
- The `<meta name="robots" content="noindex, nofollow">` tag asks search engines not to list the page.

## 10. What's demo data vs. real

On first load, the app seeds a realistic example week so you can see how everything works: a couple of sample "School Homework" items (clearly labeled **Demo example** so they're never mistaken for something Liya's actual teacher assigned), a placeholder reading book, and a placeholder achievement. Edit or delete any of it from Parent Mode — none of it is required to keep. Go to **Parent → Settings & Data → Reset to Demo Data** any time you want to start over from that same example state (this replaces all current data, so export a backup first if you want to keep what you've entered).
