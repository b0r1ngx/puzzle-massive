# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!--
Not every commit is added to this list, but many items listed are taken from the
git commit messages (`git shortlog 2.3.2..origin/develop`).

Types of changes

- **Added** for new features.
- **Changed** for changes in existing functionality.
- **Deprecated** for soon-to-be removed features.
- **Removed** for now removed features.
- **Fixed** for any bug fixes.
- **Security** in case of vulnerabilities.

## [Unreleased] - ...
-->

## [Unreleased] - ...

### Changed

- Optimized piece movement requests and moved piece movement latency to
  secondary menu on puzzle page.

## [2.8.1] - 2020-06-23

### Changed

- Show recently completed puzzle pieces
- Purge cache when puzzle status changes

### Fixed

- Fix rebuild freeze when using archive_and_clear

## [2.8.0] - 2020-06-20

Puzzle instance improvements and puzzle alert messages. Closes [#68](https://github.com/jkenlooper/puzzle-massive/issues/68).
Updated the development.md guide to be more user friendly.

### Changed

- Deleting puzzle instances that are not complete depends on last modified date
  and has a max dot cost of 1000. Puzzles that haven't been modified for
  a while can be deleted without costing any dots.
- Puzzle alerts when site goes down for maintenance as well as when the puzzle
  is being updated that would require players to reload.
- Update earned dots amount logic for piece joins. Unlisted puzzles do not earn any dots. However, the points for the player's score is still increased the same way as before. Earned dots are more closely aligned with the skill level range.
- Site settings include things that use to be set in constants.py.

### Added

- Players with an open puzzle instance slot can create copies of puzzles. These
  copies will copy the current piece positions of the source puzzle. The copy
  can not be publicly listed on the site since that would be confusing for
  players.
- Puzzle instances can have their piece positions reset by the owner at any
  time. Publicly listed puzzle instances can't have pieces reset since that
  would not be nice to other players.
- Show player puzzles other then just puzzle instances owned by that player.

### Fixed

- [Database locked issue](https://github.com/jkenlooper/puzzle-massive/issues/67) when running other scripts.
  All other apps connect to the sqlite database in read only mode. Chill app is
  the exception, but it doesn't write to the database. Scheduler will retry
  every 5 minutes if a http connection error happens when hitting the internal
  API URLs.
- Puzzles that have been recently modified show their recent status faster in
  the active puzzle list. The scheduler interval is every second now instead
  of every minute.

## [2.7.0] - 2020-05-17

### Changed

- Redesign of puzzle front page layout and header
- Update buttons to use new style
- Shorten auto-rebuild interval to keep at least the minimum amount of active
  puzzles per skill level. Did a hotfix on the live site (2020-05-10).

### Added

- Link to Puzzle Massive store which is currently a square site that allows
  players to buy puzzle instance slots.
- Style guide page when developing

## [2.6.1] - 2020-05-05

### Changed

- Home page includes a better description so search engines can index the site
  better.

### Fixed

- Hotlinking policy in web server config is less restrictive. Social media sites
  commonly add a query param to the pages that are shared. Did a hotfix on
  the live site to fix this (2020-05-04).

## [2.6.0] - 2020-05-03

Breaks everything, maybe. Then fixed everything, hopefully. Now more up to
date to the latest [jkenlooper/cookiecutter-website](https://github.com/jkenlooper/cookiecutter-website).

### Added

- New Puzzle Massive logo added to source-media.
- New favicon
- New open graph shareable image
- Included sponsor's online stores on buy stuff page.

### Changed

- More pages on the site are friendly to search indexing robots.
- Merge web server configs and clean up. Document pages go to /d/ route.
- Image upload size limit increased.
- Dropped piece movement rate restrictions per IP. Players on a shared VPN
  should have less errors once they claim or register their player account. The
  karma rules still apply per puzzle for IPs.
- Shorten player name automatic approval time to about 10 minutes.
- Improved footer layout and links.

## [2.5.2] - 2020-03-30

### Fixed

- Corrected adjacent piece logic when the piece group id is 0

## [2.5.1] - 2020-03-26

### Fixed

- Improved code to avoid causes of multiple immovable piece groups. These fixes
  were not 100% confirmed to fix the possible causes of this bug
  ([issue #63](https://github.com/jkenlooper/puzzle-massive/issues/63)).

  A python script
  ([fix_immovable_piece_groups_in_redis.py](api/api/jobs/fix_immovable_piece_groups_in_redis.py))
  was added to better find puzzles with the problem.

### Changed

- Hide latency on completed puzzles
- Hide puzzle completed alert after 5 seconds
- Add puzzle outline background color back in

## [2.5.0] - 2020-02-22

Cleaned up _some_ of the code around puzzle piece movements.

### Changed

- Switch from websockets to server-sent events for piece movement updates
- Show puzzle outline on top layer
- Refactor piece moving, joining, and stacked logic
- Allow selected piece to stay selected even when the group it is in moves

### Added

- Show latency in bottom right of outline
- Show message when puzzle is completed, frozen, or deleted

## [2.4.1] - 2020-01-05

### Added

- A toggle button on the puzzle page will draw a box around each piece that is
  still movable. This will help players find hidden pieces that blend into the
  background.

### Fixed

- Cache on message, and puzzle resources has been corrected

### Changed

- The piece count list on search page now matches the skill level range for
  queued puzzles. Players will still see their previous selection since it is
  stored in localStorage.
- Use the submitted description for Unsplash photos and fallback to description
  from Unsplash if missing. Sometimes Unsplash photos have strange
  descriptions for their photos.
- The puzzle page now shows bit icons with the player names next to
  their piece movements.

## [2.4.0] - 2019-12-14

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
