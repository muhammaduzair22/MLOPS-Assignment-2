Project Report: Streamlining Data Extraction, Transformation, and Versioned Storage
Objective:
This project aims to streamline the processes of data extraction, transformation, and versioned storage by implementing Apache Airflow. The focus lies on extracting data from dawn.com and bbc.com, performing fundamental transformation tasks, and storing the processed data on Google Drive using DVC for version control.

Workflow:
Data Extraction:

Employed Python's requests library to retrieve HTML content from dawn.com and bbc.com.
Utilized BeautifulSoup (bs4) for parsing HTML and extracting links, article titles, and descriptions from the websites' homepages.
Data Transformation:

Incorporated a placeholder function transform() for potential data transformation tasks.
Designed for preprocessing steps such as text cleaning and normalization. Currently, it functions as a placeholder printing "Transformation".
Data Loading:

Integrated a placeholder function load() for data loading operations.
Intended for saving preprocessed data to a suitable storage medium. Currently, it functions as a placeholder printing "Loading".
DVC Setup:

Installed DVC using pip install dvc.
Initialized DVC in the project directory with dvc init.
Configured a remote storage named mydrive for Google Drive using dvc remote modify.
Pushed data files to DVC cache and remote storage with dvc push.
Version Control with DVC:

Ensured metadata versioning by committing changes using dvc commit.
Each push to DVC was accompanied by a metadata versioning commit to effectively track changes.
Challenges Encountered:
Installation and Setup:

The initial setup of Airflow, DVC, and necessary libraries required meticulous configuration for compatibility and functionality across platforms, particularly on Windows.
Overcame challenges related to module dependencies, path configurations, and system compatibility during the setup phase.
Remote Storage Configuration:

Configuring remote storage with Google Drive via DVC demanded attention to syntax and path formats.
Faced errors concerning URL formatting and storage path definitions, which were resolved through iterative adjustments and consulting DVC documentation.
Version Control Integration:

Integrating DVC for version control alongside Airflow presented challenges due to differences in workflow paradigms and tool configurations.
Ensured proper synchronization between Airflow DAG tasks and DVC commands to maintain consistency in data processing and version control.
Conclusion:
This project effectively automated data extraction, transformation, and version-controlled storage using Apache Airflow and DVC. Challenges encountered during setup and integration were addressed through careful configuration and referencing documentation. The established workflow provides a solid foundation for scalable and reproducible data processing pipelines, enabling efficient management of data assets and version tracking.
