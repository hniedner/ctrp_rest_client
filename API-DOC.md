##Basic API Mechanics

Field "searching":

**The API only allows EXACT matching against the various fields.**  
* For example you can not ask for the trials that have the word "Cessation" in the "brief_title" field.  You can only match trials that have "Genetically Informed Smoking Cessation Interventions in Helping People Quit Smoking" as the title.

**The API allows for "searching" across multiple fields, multiple fields are matched using the boolean AND operator.**  
* You CAN find any trials where the trial is ONLY "Phase IV" AND it is "Active".
* You CANNOT find all the trials that are EITHER "Phase IV" OR "Active".

**The API allows for "searching" multiple times against a single field, matches against a single field are matched using the boolean OR operator.**  
* You CAN find any trial where the trial has EITHER a study site in "Texas" OR a study site in "Arkansas".  

**Both of the matching techniques can be combined**
* For example you could ask for any trial that is "Active" AND is "Phase III" OR "Phase II"

**There is a special "_fulltext" parameter that will perform a full-text search against all of the following fields of a clinical trial:**
* ID Fields (nct_id, nci_id, ccr_id, etc)
* Disease Names
* Brief Title
* Brief Summary
* Official Title
* Detailed Description
* Trial Site Organization:
  * Names
  * City
  * State or Province
    * Note the search only uses two-letter state codes. 
    * A full-text search of "Maryland" results in 247 trials 
    * A full-text search of "md" results in 1250 trials
    * And filtering on the actual study sites with the two-letter code of MD results in 1096 trials
* Collaborator Names
* Principal Investigator Names
* The names of interventions that are of an intervention type Drug

##Advanced Search Analysis

**Assumptions**
* For the purpose of this document we will define the term "View-able Trials" as to those that would be searchable by the trials.cancer.gov interface.  A trial is considered "View-able"  if it has a "current_trial_status" of:
  * Active
  * Approved
  * Enrolling by Invitation
  * In Review
  * Temporarily Closed to Accrual
  * Temporarily Closed to Accrual and Intervention
* As the trials change from day to day, the trials.cancer.gov team needs to avoid hard-coding lists that would grow or shrink over time.  For example, the various trial phases is a stable listing
* Firstly, the list of Phases is static.
* Secondly, while the "View-able Trials" may vary from day to day, the likelihood that there would be any phases without "View-able Trials" would be very low.   
