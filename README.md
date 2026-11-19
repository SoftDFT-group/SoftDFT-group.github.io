# SoftDFT website

Source of the SoftDFT project site, served by GitHub Pages at <https://softdft-group.github.io>.

The site is plain HTML/CSS at the repository root (no Jekyll; `.nojekyll` is present).
Page bodies live in `_build/pages/*.html`, example entries in `_build/examples.py`, and
`_build/build.py` wraps them in the shared header/footer.

## Edit and rebuild

```powershell
python _build/build.py                                   # rebuild HTML from _build/
python _build/build.py <Research\example> <SoftDFT code> # also refresh example input files
python _build/make_figures.py <Research\example>         # regenerate example figures
python -m http.server 8765                               # preview at http://127.0.0.1:8765
```

Site-wide settings (source-repository link, site URL, year) are at the top of `_build/build.py`.

## Publish (first time)

The account `SoftDFT-group` is a GitHub *user* account, so its Pages repository must be named
exactly `SoftDFT-group.github.io`.

1. Sign in to GitHub as **SoftDFT-group** and create a new **public**, empty repository named
   `SoftDFT-group.github.io` (no README, license or .gitignore).
2. From this folder:

   ```powershell
   git init -b main
   git add .
   git commit -m "Initial SoftDFT website"
   git remote add origin https://github.com/SoftDFT-group/SoftDFT-group.github.io.git
   git push -u origin main
   ```

3. In the repository on GitHub: **Settings → Pages → Build and deployment → Source: Deploy from a
   branch**, Branch **main**, folder **/ (root)**, **Save**.
4. After a minute or two the site is live at <https://softdft-group.github.io>.

## Update later

```powershell
python _build/build.py
git add -A
git commit -m "Update site"
git push
```

## NMSU brand

The NMSU logo is not used for now; the header names the university in plain text. If NMSU
Marketing & Communications (mktgserv@nmsu.edu) approves its use, follow <https://brand.nmsu.edu>:
show the mark unaltered at the top of every page, link it to nmsu.edu, keep it at least 75 px tall,
and keep clear space around it.
