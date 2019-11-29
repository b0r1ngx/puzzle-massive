# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!--
Not every commit is added to this list, but many items listed are taken from the
git commit messages (`git shortlog 2.3.2..origin/develop`).
-->

## [Unreleased]

Redesign with a new puzzle search page. Old queue page has been replaced.

Added the ability for players to add a name for their bit icon. Players can also
register their e-mail address with their account. Login by e-mail can then be
accomplished by going through a reset login process.

New puzzle instances and slots are a new paid for feature, but not automated at
the moment.

### Changed

- New players are shown a new player page
- Show player id in base 36 for no bits
- Add shareduser to user flow, drop cost to bit icon
- Limit to active puzzles, use a queue for others
- Show approved username next to bit

### Added

- Puzzle instances and puzzle slots
- Support for puzzle variants
- Document use of chill dump and chill load
- Allow player instance puzzles to be unlisted
- Add player detail view for admin
- Show pieces when puzzle is frozen
- Add puzzle list page
- Add puzzle image card
- Add testdata script
- Add bump button for moving queue puzzles
- Add player email form on profile page
- Show total active players near footer
- Add email verification and player claim
- Add menu and clean up profile page
- Setup for reset login by email form

### Removed

- Deprecate puzzle queue pages and redirect
- Remove up/down buttons for pm-ranking

### Fixed

- Extend user cookie expiration correctly
- Fix error for first piece move on puzzle

## [2.3.2] - 2019-07-26

Run janitor task after pieces request finish.

## [2.3.1] - 2019-06-11

Minor changes to homepage and auto rebuild handling of puzzles.

## [2.3.0] - 2019-05-28

Switch to python 3. Improve development guide.

### Added

- Scheduler process to auto rebuild and other tasks
- Add redis keys for tracking score/rank
- Replace player-ranks api
- Add total player count and active players

### Fixed

- Improve cleanup of completed puzzles

## [2.2.0] - 2019-03-21

Start using web components and typescript.

### Added

- Add prettier package
- Add stylelint
- Make the domain name configurable
- Improve docs for developing and deploying
- Show license in footer, update contribute info
- Show message for unsupported browsers
- Store anonymous login link locally
- Add logout link

### Removed

- Old angularJS code has been replaced
- Remove minpubsub

### Deprecated

- Drop support for older browsers

### Fixed

- Fix error with concurrent pieces alert
- Fix missing bit icon

## [2.1.4] - 2019-02-03

Improved build process for JS. Cleaned up the README and development guide.

## [2.1.3] - 2019-01-20

### Added

- Set rebuild puzzle to change piece count
- Implement rebuild status

## [2.1.2] - 2019-01-15

Include a note to update policy on image magick when creating a new server. This
allows the puzzle generating process to create larger puzzles.

### Fixed

- Prevent reset of puzzles that used old render
- Fix query on puzzle reset

## [2.1.1] - 2019-01-12

### Fixed

- Remove check for immovable on token request
- Fix migrate puzzle file script

## [2.1.0] - 2019-01-08

### Added

- Improved puzzle upload handling.
- Add checks for puzzle piece movements.

## [2.0.1] - 2018-10-28

Clean up some documentation on deployment instructions. Fix some minor issues
with SQL on queue page.

## [2.0.0] - 2018-10-06

Started a new direction for this project to be more open and now hosted on
GitHub.

### Moved

- Migrate all files from GitLab repo