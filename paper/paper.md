---
Title: 'PyToughReact – A Python Package for automating reactive transport and biodegradation simulations.'

Tags:
  - Python
  - reactive transport
  - uncertainty quantification
  - sensitivity analysis
  - TOUGH, PyTOUGH

Authors:
  - Name: Temitope Ajayi 
orcid: 0000-0002-0782-7460
    affiliation: 1 
  - Name: Ipsita Gupta
    affiliation: 1

Affiliations:
 - Name: Louisiana State University, USA
 - Index: 1

Date: 17 May 2022

Bibliography: paper.bib

# Summary

This package provides a tool for researchers in the reactive transport community to automate their simulations 
with the TOUGH family of codes especially for uncertainty quantifications and sensitivity analysis. Currently, this 
package has the ability to automate reaction and biodegradation reactions using both TMVOCBIO and TOUGHREACT.

# Statement of need

The suite of TOUGH simulators by the Lawrence Berkeley National Laboratory (LBNL) are well known simulators 
for flow and transport simulations. In order to model chemical reactions coupled to flow for isothermal and 
non-isothermal systems, the TOUGHREACT simulator exists. In addition, the TMVOC software exists for the modeling 
of multicomponent mixtures of volatile organic compounds suitable for contamination problems. When biodegradation 
is added to the process, the tool used is known as TMVOC-BIO. These reaction simulators as is now do not provide a 
tool to automatically run many simulations for tasks such as uncertainty quantification or sensitivity analysis. 
Users need to create many simulation folders to run every sensitivity they intend to run with the simulator. 
This makes it cumbersome to use and users could get lost on the purpose of each folder if not correctly labeled. 
While PyTOUGH and TOUGHIO exists for regular flow and transport simulations, no such tool exists for chemical and 
biodegradation reactions, `PyToughReact` fulfills this need for users familiar with python.


# Citations

Citations to entries in paper.bib should be in
[rMarkdown](http://rmarkdown.rstudio.com/authoring_bibliographies_and_citations.html)
format.

If you want to cite a software repository URL (e.g. something on GitHub without a preferred
citation) then you can do it with the example BibTeX entry below for @fidgit.

For a quick reference, the following citation commands can be used:
- `@author:2001`  ->  "Author et al. (2001)"
- `[@author:2001]` -> "(Author et al., 2001)"
- `[@author1:2001; @author2:2001]` -> "(Author1 et al., 2001; Author2 et al., 2002)"


# Acknowledgements

Funding for this research is from the National Academy of Sciences, Engineering, and Medicine (NASEM) Gulf Research 
Program (GRP) grant on “Mitigating Risks to Hydrocarbon Release through Integrative Advanced Materials for Wellbore 
Plugging and Remediation” under award number 200008863 and the Early Career Research Fellowship of Ipsita Gupta. 

# References