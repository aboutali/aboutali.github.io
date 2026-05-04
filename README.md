# aboutali/aboutali

Source for [aboutali.github.io](https://aboutali.github.io/) — a master index
of all my projects.

The site is a single static `index.html` styled like a 1996 Netscape page.
No build, no JS, no dependencies.

## Adding a new project

1. Open `index.html`.
2. Find the block between `<!-- PROJECTS:BEGIN -->` and `<!-- PROJECTS:END -->`.
3. Add a new `<li>` (followed by `<br>`):

   ```html
   <li>
     <b><a href="https://aboutali.github.io/REPO/">REPO</a></b>
     <font size="2">[<a href="https://github.com/aboutali/REPO">source</a>]</font><br>
     One-sentence description.
   </li>
   <br>
   ```

4. Replace `REPO` and the description. Commit and push to `main`.

## Notes

- The Pages URL `aboutali.github.io/<repo>/` only resolves if that repo has
  GitHub Pages enabled (Settings → Pages → Source). Private repos require a
  paid plan to serve via Pages.
- `.nojekyll` is present so GitHub Pages serves files literally without
  Jekyll processing.
- Claude Code can scaffold/maintain this file — just ask it to add or remove
  a project.
