# Changelog

## [3.3.0](https://github.com/grzegorzfranus/github-workflows/compare/v3.2.0...v3.3.0) (2026-08-31)


### Features

* **ansible:** add CycloneDX SBOM generation workflow ([#73](https://github.com/grzegorzfranus/github-workflows/issues/73)) ([9a6bbdb](https://github.com/grzegorzfranus/github-workflows/commit/9a6bbdbc27a0c652e3ba54c5360f89c001abe255))

## [3.2.0](https://github.com/grzegorzfranus/github-workflows/compare/v3.1.9...v3.2.0) (2026-08-30)


### Features

* adopt the shared runner selection mechanism ([#69](https://github.com/grzegorzfranus/github-workflows/issues/69)) ([#71](https://github.com/grzegorzfranus/github-workflows/issues/71)) ([219e963](https://github.com/grzegorzfranus/github-workflows/commit/219e96385fe1acac2be278f620969a492858ce49))

## [3.1.9](https://github.com/grzegorzfranus/github-workflows/compare/v3.1.8...v3.1.9) (2026-08-30)


### Documentation

* split workflow docs, pin examples to main, unify section order ([#66](https://github.com/grzegorzfranus/github-workflows/issues/66)) ([#67](https://github.com/grzegorzfranus/github-workflows/issues/67)) ([3784fbb](https://github.com/grzegorzfranus/github-workflows/commit/3784fbb65f945eda152b266428dfb1c59c28fd8a))

## [3.1.8](https://github.com/grzegorzfranus/github-workflows/compare/v3.1.7...v3.1.8) (2026-08-30)


### CI/CD

* enable markdownlint and remove the dead scripts directory ([#63](https://github.com/grzegorzfranus/github-workflows/issues/63)) ([#64](https://github.com/grzegorzfranus/github-workflows/issues/64)) ([841cdf5](https://github.com/grzegorzfranus/github-workflows/commit/841cdf537d9972c8e50467d49a7ddd26b7f9bd1a))

## [3.1.7](https://github.com/grzegorzfranus/github-workflows/compare/v3.1.6...v3.1.7) (2026-08-30)


### Documentation

* remove the migration guides and align the pipeline sections ([#60](https://github.com/grzegorzfranus/github-workflows/issues/60)) ([#61](https://github.com/grzegorzfranus/github-workflows/issues/61)) ([7e822b7](https://github.com/grzegorzfranus/github-workflows/commit/7e822b71b0aba2fe5768095815cc4aaee2707dc6))

## [3.1.6](https://github.com/grzegorzfranus/github-workflows/compare/v3.1.5...v3.1.6) (2026-08-30)


### Documentation

* refresh README, replace husky, align workflows with the fork ([#57](https://github.com/grzegorzfranus/github-workflows/issues/57)) ([#58](https://github.com/grzegorzfranus/github-workflows/issues/58)) ([32ba59d](https://github.com/grzegorzfranus/github-workflows/commit/32ba59d3aaf35e156a93a805b38cdc8a5fc535bc))

## [3.1.5](https://github.com/grzegorzfranus/github-workflows/compare/v3.1.4...v3.1.5) (2026-08-30)


### Bug Fixes

* keep the TruffleHog action SHA and binary version pins in step ([#52](https://github.com/grzegorzfranus/github-workflows/issues/52)) ([#53](https://github.com/grzegorzfranus/github-workflows/issues/53)) ([a63cdae](https://github.com/grzegorzfranus/github-workflows/commit/a63cdae2dc68744a7da3c3cc5fde77df662db83f))


### CI/CD

* pin actions/checkout to v5.1.0 and ignore v6+ ([#55](https://github.com/grzegorzfranus/github-workflows/issues/55)) ([#56](https://github.com/grzegorzfranus/github-workflows/issues/56)) ([997da91](https://github.com/grzegorzfranus/github-workflows/commit/997da913ddbdb09e09eee4785b887efb35cd0446))

## [3.1.4](https://github.com/grzegorzfranus/github-workflows/compare/v3.1.3...v3.1.4) (2026-08-29)


### CI/CD

* adopt downstream hardening and align action pins ([#49](https://github.com/grzegorzfranus/github-workflows/issues/49)) ([#50](https://github.com/grzegorzfranus/github-workflows/issues/50)) ([7adbe3a](https://github.com/grzegorzfranus/github-workflows/commit/7adbe3a89815c763554c9a2ea20e9b21c5ee8053))

## [3.1.3](https://github.com/grzegorzfranus/github-workflows/compare/v3.1.2...v3.1.3) (2026-08-13)


### Dependencies

* **deps:** bump trufflesecurity/trufflehog from 3.95.9 to 3.96.0 in the minor-and-patch group across 1 directory ([#44](https://github.com/grzegorzfranus/github-workflows/issues/44)) ([4b35a29](https://github.com/grzegorzfranus/github-workflows/commit/4b35a2968397e332a59df937669dc46a50861d63))

## [3.1.2](https://github.com/grzegorzfranus/github-workflows/compare/v3.1.1...v3.1.2) (2026-08-12)


### Bug Fixes

* specify explicit trivy release version in ansible security workflow ([#46](https://github.com/grzegorzfranus/github-workflows/issues/46)) ([9f73a48](https://github.com/grzegorzfranus/github-workflows/commit/9f73a486097d0d229671935fa1a47ccd68374ba4))

## [3.1.1](https://github.com/grzegorzfranus/github-workflows/compare/v3.1.0...v3.1.1) (2026-07-30)


### Dependencies

* **deps:** bump trufflesecurity/trufflehog from 3.95.8 to 3.95.9 in the minor-and-patch group ([#36](https://github.com/grzegorzfranus/github-workflows/issues/36)) ([7ae55a5](https://github.com/grzegorzfranus/github-workflows/commit/7ae55a5ed44c05e010077663a5fff07e94efa139))

## [3.1.0](https://github.com/grzegorzfranus/github-workflows/compare/v3.0.1...v3.1.0) (2026-07-30)


### Features

* validate Ansible role variable consistency across defaults, argument_specs, assert and README ([#38](https://github.com/grzegorzfranus/github-workflows/issues/38)) ([67259c1](https://github.com/grzegorzfranus/github-workflows/commit/67259c1b515bee8681b1a0acb6395e7d3c00bd8c))

## [3.0.1](https://github.com/grzegorzfranus/github-workflows/compare/v3.0.0...v3.0.1) (2026-07-20)


### Miscellaneous

* align workflows with comlia platform standards ([#34](https://github.com/grzegorzfranus/github-workflows/issues/34)) ([a6a452e](https://github.com/grzegorzfranus/github-workflows/commit/a6a452e50affb3b1b4003a03f9e2763438583558))

## [3.0.0](https://github.com/grzegorzfranus/github-workflows/compare/v2.0.0...v3.0.0) (2026-07-19)


### ⚠ BREAKING CHANGES

* **workflows:** [#30] extract galaxy metadata validation ([#31](https://github.com/grzegorzfranus/github-workflows/issues/31))

### Features

* **workflows:** [[#30](https://github.com/grzegorzfranus/github-workflows/issues/30)] extract galaxy metadata validation ([#31](https://github.com/grzegorzfranus/github-workflows/issues/31)) ([e14fb85](https://github.com/grzegorzfranus/github-workflows/commit/e14fb85bf573bfdb0e0cc3a4313bb30b95d47c8b))

## [2.0.0](https://github.com/grzegorzfranus/github-workflows/compare/v1.2.5...v2.0.0) (2026-07-19)


### ⚠ BREAKING CHANGES

* **ci:** rename reusable workflows and harden CI [#27] ([#28](https://github.com/grzegorzfranus/github-workflows/issues/28))

### Features

* **ci:** rename reusable workflows and harden CI [[#27](https://github.com/grzegorzfranus/github-workflows/issues/27)] ([#28](https://github.com/grzegorzfranus/github-workflows/issues/28)) ([f680543](https://github.com/grzegorzfranus/github-workflows/commit/f68054340ea8198c692a4d3a808ab15a685dfd1b))

## [1.2.5](https://github.com/grzegorzfranus/github-workflows/compare/v1.2.4...v1.2.5) (2026-07-19)


### Bug Fixes

* **ci:** install galaxy collections in syntax-check job ([#25](https://github.com/grzegorzfranus/github-workflows/issues/25)) ([24ddab7](https://github.com/grzegorzfranus/github-workflows/commit/24ddab777ae93afe9862115777debff0064f6fdf))

## [1.2.4](https://github.com/grzegorzfranus/github-workflows/compare/v1.2.3...v1.2.4) (2026-07-03)


### Bug Fixes

* configure dependabot to trigger release-please version bumps ([#22](https://github.com/grzegorzfranus/github-workflows/issues/22)) ([6f7cf88](https://github.com/grzegorzfranus/github-workflows/commit/6f7cf88baf920eff29e1a1e39c768408bd0b74d0))

## [1.2.3](https://github.com/grzegorzfranus/github-workflows/compare/v1.2.2...v1.2.3) (2026-07-03)


### Documentation

* add workflow input tables, architecture diagram, and missing sections ([#19](https://github.com/grzegorzfranus/github-workflows/issues/19)) ([af84e2c](https://github.com/grzegorzfranus/github-workflows/commit/af84e2c6e72c840edd14dc5097075eeb67b93a35))

## [1.2.2](https://github.com/grzegorzfranus/github-workflows/compare/v1.2.1...v1.2.2) (2026-06-26)


### Documentation

* **readme:** remove agent skill references and clean up spacing ([#13](https://github.com/grzegorzfranus/github-workflows/issues/13)) ([054d872](https://github.com/grzegorzfranus/github-workflows/commit/054d8720b97eb7f4427a768da9480646ef549320))

## [1.2.1](https://github.com/grzegorzfranus/github-workflows/compare/v1.2.0...v1.2.1) (2026-06-26)


### Documentation

* **readme:** document modular reusable ansible workflows and usage ([#11](https://github.com/grzegorzfranus/github-workflows/issues/11)) ([02b7ee3](https://github.com/grzegorzfranus/github-workflows/commit/02b7ee3c5aeff55ccf672dfe1e9a67c4281c2d2a))

## [1.2.0](https://github.com/grzegorzfranus/github-workflows/compare/v1.1.2...v1.2.0) (2026-06-26)


### Features

* **ci:** add modular enterprise reusable workflows for ansible ([#9](https://github.com/grzegorzfranus/github-workflows/issues/9)) ([9925ba2](https://github.com/grzegorzfranus/github-workflows/commit/9925ba2ec21b895c77390eb120c2c817984074a1))

## [1.1.2](https://github.com/grzegorzfranus/github-workflows/compare/v1.1.1...v1.1.2) (2026-06-26)


### Bug Fixes

* **ci:** allow dependabot branches and fix skipped checks in merge gate ([#7](https://github.com/grzegorzfranus/github-workflows/issues/7)) ([2d124b2](https://github.com/grzegorzfranus/github-workflows/commit/2d124b21030982da9f46bb590ee7416e22ddba07))

## [1.1.1](https://github.com/grzegorzfranus/github-workflows/compare/v1.1.0...v1.1.1) (2026-06-26)


### Bug Fixes

* **release:** fix merge check context name and upgrade actions to node 24 ([#5](https://github.com/grzegorzfranus/github-workflows/issues/5)) ([73113bc](https://github.com/grzegorzfranus/github-workflows/commit/73113bc61575ef48112f230d8fc0dfe89848a52d))

## [1.1.0](https://github.com/grzegorzfranus/github-workflows/compare/v1.0.0...v1.1.0) (2026-06-26)


### Features

* **repo:** initialize repository with enterprise workflows and templates ([#1](https://github.com/grzegorzfranus/github-workflows/issues/1)) ([310620a](https://github.com/grzegorzfranus/github-workflows/commit/310620ab67a1f92ec81fae961c9a7a00f39c5c19))


### Bug Fixes

* **release:** update release-please-action to correct stable commit SHA ([#3](https://github.com/grzegorzfranus/github-workflows/issues/3)) ([2e44fb1](https://github.com/grzegorzfranus/github-workflows/commit/2e44fb19223b190ac6f1c49b8488212a229258ba))

## Changelog

All notable changes to this project will be documented in this file.
Releases and versioning are automatically managed by [Release Please](https://github.com/googleapis/release-please).
