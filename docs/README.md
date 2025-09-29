_As of October 2025, this project has ended and the repository is now archived._

# PeMS

Caltrans Performance Measurement System

PeMS is open-source software that is designed, developed, and maintained by [Compiler LLC](https://compiler.la) on behalf of Caltrans Traffic Operations.

## Product Roadmap

Our product roadmap captures what we're currently building, what we've built, and what we plan to build in future quarters. It is updated on a regular basis, aligned with project progress.

```mermaid
timeline
    title PeMS Product Roadmap
    %% PeMS Epics (2024)
    section 2024

    Q3<br>Complete
    : Project launch
    : Established resources and overall scope
    : Began discovery work

    Q4<br>Complete
    : Confirm site architecture
    : Set up GitHub repository
    : Scaffold app structure
    : Create a prioritized backlog of features
    : Created local environment

    %% PeMS Epics (2025)
    section 2025

    Q1<br>Complete
    : Project paused for AWS license approval

    Q2<br>Now
    : Create dev environment
    : Create test environment
    : Launch test version of district-specific pages
    : Set up a working CI/CD pipeline

    Q3<br>Planned
    : Create production environment
    : User testing for district-specific pages and initial features (early Q3)
    : Launch test version of full site
    : Additional user testing for full site (timing TBD)

    Q4<br>Future
    : Go-Live - Date TBD
    : Compiler contract for PeMS ends September 2025, but planning to extend to Dec. 2025

    %%{
        init: {
            'logLevel': 'debug',
            'theme': 'default' ,
            'themeVariables': {
                'cScale0': '#ffa500', 'cScaleLabel0': '#000000',
                'cScale1': '#ffff00', 'cScaleLabel1': '#000000',
                'cScale2': '#ffff00', 'cScaleLabel2': '#000000',
                'cScale3': '#008000', 'cScaleLabel3': '#ffffff',
                'cScale4': '#0000ff', 'cScaleLabel4': '#ffffff',
                'cScale5': '#4b0082', 'cScaleLabel5': '#ffffff',
                'cScale6': '#000000', 'cScaleLabel6': '#ffffff'
            }
        }
    }%%
```
