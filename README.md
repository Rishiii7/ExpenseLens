# ExpenseLens - A smart expense management system


## Description
We plan to develop an intelligent expense management system that streamlines expenditure tracking, enabling users to effortlessly organize their daily expenses and analyze their expenditure trends. We intend to implement an OCR component to capture relevant information from receipts and invoices, further utilizing a data categorization module that would extract essential entities such as vendor details, product information, transaction date and amount, etc. and categorize each of these expenses based on personalized expense categorization features. Lastly, we would provide the user with an analytics dashboard that gives real-time insights into their spending habits and expenditure trends.

## Key components:
Containers - To host the OCR and data categorization modules as microservices
Storage Service - to store receipts, invoices, etc.
Database - to store categorized expenses along with additional metadata.
Key-value store - for storing temporary data during the processing of receipts, eventually allowing quick access during the categorization process.
RPC/API Interface - to facilitate communication between the OCR module, the data categorization module, and the database

## Team members: Prachitee Maratkar, Rishikesh Sangamanath Solapure
