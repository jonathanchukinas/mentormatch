# Validatation Rules for Mentoring Applications saved to Excel
## Excel Workbook
You can name your Excel workbook anything you like.
`mentormatch` will present you with a `file open` dialog so you can pick the appropriate file.  
## Excel Worksheets
`mentormatch` looks for two worksheets: `mentors` and `mentees`.

Each worksheet is subject to the following rules:
- Field Names (aka Headers) must be in the first row. 
- The first header must be in the first column ...??TRUE??
- The order of the headers is unimportant.
- Required headers must not be repeated. 
  Example: `mentormatch` expects to find a `wwid` header in the first row of each worksheet.
    If the `mentees` worksheet contains two `wwid` headers, `mentormatch` will throw an error. 

## Terminology
- **RECORD**: an Excel row containing one individual's application. Each worksheet can contain hundreds of records.
  The first row though is *not* a record. The first Excel row should contain only Field Names.
  - Synonyms: Row, Mentoring Application
- **FIELD**: an Excel column. The first cell in the column contains the Field Name. 
  All cells below that contain the same type of information.
  Example: Both `mentors` and `mentees` worksheets should both contain a `wwid` field. 
  The word `wwid` appears in the first row. The WWIDs appearing below that are all integers and belong to.
  - Synonyms: Column, Header
  - *Mentor WWIDs* example: On the `mentors` worksheet, the string `wwid` must appear somewhere in the first row. 
    The cells below that contain the WWIDs of the various mentor applicants.

## Rules
### General Rules
- All records must be contained within one Excel workbook.
- All mentor records must be on a worksheet named `mentors`; 
  all mentee records on a worksheet named `mentees`.
- All Field names must be in first row (Row 1). 
- `mentors` and `mentees` must be **blank** below the last record. 
  Example: if there are 100 mentor applcants, **all** cells in rows 102 and beyond should be blank/empty.
- `mentors` and `mentees` must contain all their required functional fields. See below.
- `mentormatch` is case-insensitive. 
  This means that a mentee looking for a `Female` mentor can be matched with a `female` mentor.
- Field Names are case-insensitive but must be spelled exactly as given in the Functional Fields table below.

### Field-Specific Rules
- `gender`, `gender_pref_yes` and `gender_pref_maybe`: 
  - `gender` is the gender of the current applicant.
  - `gender_pref_yes` are the genders this applicant would like to be paired with. 
  - For `gender_pref_yes` and `gender_pref_maybe`, multiple genders need to be comma-separated. A single gender may contain a trailing comma.
  - This applicant might also be paired with someone whose gender is in the `gender_pref_maybe` field if a better match could not be found.
  - A gender that appears as both 'yes' and 'maybe' will be treated as a 'yes'
- `site`, `site_pref_yes`, and `site_pref_maybe` are subject to the same rules as gender.
- `years` is the number of years a person has worked professionally. The value may be an integer or a floating point number. 'Years at J&J' is not evaluated by `mentormatch`.
- `position_level` must be an integer between 2 and 6, inclusive.
- `priority` (optional) gives the Mentoring Committee the ability to give preferential treatment to one or more mentor/ees. 
  Most commonly, this is done to prevent applicants from being rejected two years in a row.
  - `0` or `BLANK` = no special treatment. This should be most applicants. 
  - `1` makes it much more likely that this applicant will get paired.
  - `2` makes it **that much more** likely to be paired.
  - etc. Note: the size of the integer doesn't matter, only the rank order.
  - Remember, most applicants should be at zero priority for this to properly work.
- `wants_random_mentor` (mentee only). Empty cells, `0`, and `False` all evaluate to 'False'. All else evaluates to 'True'.
- `wwid_pref`: (mentee only) Each non-consecutive integer is extracted as a WWID. 
  WWIDs appear in ranked order, from most preferred to least preferred.
  - Valid: `1111111`, `1111111, 2222222, 3333333`, `BLANK`, `1111111 2222222,3333333,,, ,,,,,`.
  - Special case: If no WWIDs are extracted from the cell value, `wants_random_mentor` will be forced to `True`.
- `max_mentee_count` (mentor only) should be greater than or equal to one.

### Functional Fields

Worksheets `mentors` and `mentees` must contain the fields shown below according to this legend:
- R = required
- O = optional
- \- = meaningless on this worksheet.

| Header | `mentors` | `mentees` | Type |
| ------ |: ---------- :|: ----- :|: ----- |
| `wwid` | R| R| Integer
| `gender` | R| R| String | 
| `site` | R  | R| String
| `years` | R| R| Integer or Float
| `position_level` | R| R| Integer between 2 and 6
| `genders_pref_yes` | R| R | Comma-separated String
| `sites_pref_yes` | R| R | Comma-separated String
| `max_mentee_count` | R| - | Non-negative Integer
| `wwid_pref` | - |R| Blank, or single Integer, or comma/space-separated list of Integers
| `wants_random_mentor`| -| R| True or False
| `sites_pref_maybe`| O | O | Comma-separated String
| `genders_pref_maybe`| O| O | Comma-separated String
| `priority` | - | O | Non-negative Integer
