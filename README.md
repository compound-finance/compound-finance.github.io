# Comet Docs Website

The Compound III documentation website is a [Jekyll](https://jekyllrb.com/) site hosted by GitHub pages at https://c3-docs.compound.finance/.

To modify the website, make a pull request here.

## Running Locally

1. Install [Ruby](https://www.ruby-lang.org/en/documentation/installation/)
2. **Fork and then clone** this repository
3. Navigate to the `docs/` folder
4. Run the `bundle` command to install Jekyll dependencies.
5. Run the serve command to host the site on a locally hosted web server.
7. Use a web browser and navigate to `http://localhost:4000/`
6. Edit, save files and refresh the localhost page to see the effects of code changes.

```
## Install Ruby first

## Make sure you FORK the repository so you can make a pull request later
git clone git@github.com:my-github-username/compound-finance.github.io.git

## Navigate to the Jekyll app folder
cd compound-finance.github.io/docs/

## Get the Ruby dependencies for Jekyll to work
bundle

## Serve the source files to a local web server
jekyll serve
```

## Changes

Documentation text can be edited by modifying the markdown files in the `docs/pages/` folder.

Page layout HTML, CSS, and JavaScript can be found in `_layouts/`, `_includes/`, and `public/`.

When you are ready to merge your changes, make a pull request into this repository.

## Technologies Used

- HTML, CSS, JavaScript
- Jekyll
- Highlight.js (Syntax highlighting)
- highlightjs-solidity (Syntax highlighting)
