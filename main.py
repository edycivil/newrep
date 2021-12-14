import sqlite3
from sqlite3.dbapi2 import connect
from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

# Router
@app.get("/")
def root():
  return {"message": "It works !"}

#Company payload example
#{ 
# "Name"            :   "Meta",
# "AddressCountry"  :   "USA",
# "AddressState"    :   "LA",
# "AddressCity"     :   "sillicon valley",
# "AddressStreet"   :   "Beautiful Street",
# "AddressNumber"   :   "546",
# "AddressPostCode" :   "10200",
# "Company_VATID"   :   "2131231434123",
# "BankAccName"     :   "MetaCorp",
# "BankAccNumber"   :   "1225345345345"
#}

#---function allows companies to create an account and record their information if they already doesn't have an account 

@app.post("/create_company_account")
async def create_company_account(payload: Request):
  values_dict = await payload.json()
  dbase = sqlite3.connect('database_group43.db', isolation_level=None)
  dbase.execute('''
    INSERT INTO Company(
    Company_Name,
    Company_AddressCountry,
    Company_AddressState,
    Company_AddressCity,
    Company_AddressStreet,
    Company_AddressNumber,
    Company_AddressPostCode,
    Company_VATID, 
    Company_BankAccName,
    Company_BankAccNumber)
    VALUES(
    {Company_Name},
    {Company_AddressCountry},
    {Company_AddressState},
    {Company_AddressCity},
    {Company_AddressStreet},
    {Company_AddressNumber},
    {Company_AddressPostCode},
    {Company_VATID}, 
    {Company_BankAccName},
    {Company_BankAccNumber})
    '''.format(
    Company_Name=                 str(values_dict['Company_Name']),
    Company_AddressCountry=       str(values_dict['Company_AddressCountry']),
    Company_AddressState=         str(values_dict['Company_AddressState']),
    Company_AddressCity=          str(values_dict['Company_AddressCity']),
    Company_AddressStreet=        str(values_dict['Company_AddressStreet']),
    Company_AddressNumber=        str(values_dict['Company_AddressNumber']),
    Company_AddressPostCode=      str(values_dict['Company_AddressPostCode']),
    Company_VATID=                str(values_dict['Company_VATID']), 
    Company_BankAccName=          str(values_dict['Company_BankAccName']),
    Company_BankAccNumber=        str(values_dict['Company_BankAccNumber'])))

  dbase.close()
  return True

#dbase = sqlite3.connect('database_group43.db', isolation_level=None)
#print(dbase.execute('''SELECT * FROM Comapny'''.fetchall()))
#dbase.close()





#Customer payload example
#{ 
#  "Name": "Bond",
#  "Surname":"James",
#  "Customer_Birthdate"
#  "Email":"james.bond@gmail.com",
#  "AddressCountry":"USA",
#  "AddressState": "Statexyz",
#  "AddressCity": "Cityxyz",
#  "AddressStreet": "Streetxyz",
#  "AddressNumber": "101",
#  "AddressPostCode": "1020",
#  "CCNumber": "2233 4455 6677 8899",
#}

#---function allows customers to create an account and record their information if they already doesn't have an account 

@app.post("/create_customer_account")
async def create_customer_account(payload: Request):
  values_dict = await payload.json()
  #open DB 
  dbase = sqlite3.connect('database_group43.db', isolation_level=None)
  # Retrieve customer on email address
  query_Customer = dbase.execute(''' 
                    SELECT ID FROM Customer
                    WHERE Email = {Email}               
                    '''.format(Email=str(values_dict['Email'])))
  # We then store the results of the query with fetchall.
  Customer_results = query_Customer.fetchall()
  # Check condition: no customer found
  if len(Customer_results) == 0:
  # Create new customer
      dbase.execute('''
        INSERT INTO Customer(
       Customer_Name,
       Customer_Surname,
       Customer_Email,
       Customer_AddressCountry,
       Customer_AddressState,
       Customer_AddressCity,
       Customer_AddressStreet,
       Customer_AddressNumber,
       Customer_AddressPostCode, 
       Customer_CCNumber)
       Customer_VALUES(
            {Company_Name},
            {Company_Surname},
            {Company_Email},
            {Company_AddressCountry},
            {Company_AddressState},
            {Company_AddressCity},
            {Company_AddressStreet},
            {Company_AddressNumber},
            {Company_AddressPostCode},
            {Company_CCNumber})     
        '''.format(
          Customer_Name=               str(values_dict['Customer_Name']),
          Customer_Surname=            str(values_dict['Customer_Surname']),
          Customer_Email=              str(values_dict['Customer_Email']),
          Customer_AddressCountry=     str(values_dict['Customer_AddressCountry']),
          Customer_AddressState=       str(values_dict['Customer_AddressState']),
          Customer_AddressCity=        str(values_dict['Customer_AddressCity']),
          Customer_AddressStreet=      str(values_dict['Customer_AddressStreet']),
          Customer_AddressNumber=      str(values_dict['Customer_AddressNumber']),
          Customer_AddressPostCode=    str(values_dict['Customer_AddressPostCode']),
          Customer_CCNumber=           str(values_dict['Customer_CCNumber'])))
          
  # Create new customer account 
  query_Customer = dbase.execute('''
                            SELECT ID FROM Customer
                            WHERE Email = {Email}
                            '''.format(Email=str(values_dict['Email'])))
  # Store ID with fetchall, found in row 0 col 0
  customerID = query_Company.fetchall()[0][0]
  dbase.execute('''
        INSERT INTO CustomerAccounts(
        CompanyID,
        CustomerID)
        VALUES(
            {CompanyID},
            {CustomerID})  
        '''.format(
          CompanyID=str(values_dict['CompanyID']),
          CustomerID=str(customerID)))
  #close DB 
  dbase.close()
  return True

#Quote payload example
#The function's name is "create_subscription" but it's still a quote at this point. It becomes a subscription when Active = 1, in the "convert_quote" section
#{ 
#  "CustomerAccountID": "1",
#  "ProductID":"1",
#  "Quantity": "2",
#  "StartDate": "01-01-2022",
#  "EndDate": "01-01-2023"
#}
@app.post("/create_subscription")
async def create_subscription(payload: Request):
  values_dict = await payload.json()
  #open DB
  dbase = sqlite3.connect('database_group43.db', isolation_level=None)
  #TotalPrice calculator 
  query_price = dbase.execute(''' 
                    SELECT priceLocal FROM Products
                    WHERE ProductID = {ProductID}               
                    '''.format(ProductID=str(values_dict['ProductID'])))
  PriceLocal = query_price.fetchall()[0][0]
  Quantity = values_dict['Quantity']
  TotalPriceLocalVATE = Quantity*PriceLocal
  TotalPriceLocalVATI = TotalPriceVATE*1,21
  #Create subscription
  dbase.execute('''
    INSERT INTO Subscriptions(
    CustomerAccountID,
    ProductID,
    Quantity, 
    TotalPriceLocalVATE,
    TotalPriceLocalVATI,
    StartDate,
    EndDate)
    VALUES(
        {CustomerAccountID},
        {ProductID},
        {Quantity},
        {TotalPriceLocalVATE},
        {TotalPriceLocalVATI},
        {StartDate},
        {EndDate})
        '''.format(
          CustomerAccountID=      str(values_dict['CustomerAccountID']),
          ProductID=              str(values_dict['ProductID']),
          Quantity=               str(values_dict['Quantity']),
          TotalPriceLocalVATE=    str(TotalPriceLocalVATE),
          TotalPriceLocalVATI=    str(TotalPriceLocalVATI),
          StartDate=              str(values_dict['StartDate']),
          EndDate=                str(values_dict['EndDate'])))
  dbase.close()
  return True

#Review quote payload example
#We assume the customer knows the subscrptionID
#Acceptance = 2 -> refused
#Acceptance = 1 -> accepted
#Acceptance = 0 -> not reviewed yet
#{ 
#  "SubscriptionID":"1",
# "Acceptance":"1"
#}
@app.post("/review_quote")
async def review_quote(payload: Request):
  values_dict = await payload.json()
  #open DB
  dbase = sqlite3.connect('database_group43.db', isolation_level=None)
  
  dbase.execute(''' 
    UPDATE Subscription
    SET Acceptance = {Acceptance}
    WHERE SubscriptionID = {SubscriptionID}  
    '''.format(Acceptance = values_dict['Acceptance'], SubscriptionID = values_dict['SubscriptionID']))
  dbase.close()
  return True

#Convert quote payload example
#{ 
#  "CompanyID": "1"
#. "SubscriptionID": "5"
#}
@app.post("/convert_quote")
async def convert_quote(payload: Request):
  values_dict = await payload.json()
  #open DB
  dbase = sqlite3.connect('database_group43.db', isolation_level=None)                                         
  
  dbase.execute(''' 
      UPDATE Subscriptions
      SET Active = 1
      WHERE SubscriptionID = {SubscriptionID}  
      '''.format(SubscriptionID = values_dict["SubscriptionID"]))
  dbase.close()
  return True

#Create invoice payload example
#{ 
#  "CustomerAccountID": "1",
#  "InvoiceDate": "2022-01-31",
#  "CompanyID": "1"                                                       
#}
@app.post("/create_invoice")
async def create_invoice(payload: Request):
  values_dict = await payload.json()
  #open DB
  dbase = sqlite3.connect('database_group43.db', isolation_level=None)
  query_subscriptions = dbase.execute('''
                            SELECT TotalPriceLocalVATI FROM Subscriptions
                            WHERE Active = 1 AND CustomerAccountID = {CustomerAccountID} AND {InvoiceDate} BETWEEN StartDate AND EndDate
                            '''.format(CustomerAccountID=values_dict['CustomerAccountID']), InvoiceDate=str(values_dict['InvoiceDate']))
  subscriptions_results = query_subscriptions.fetchall()
  
  TotalDueEuro = 0
  for subscription in subscriptions_results:
    TotalDueEuro += subscription[0]
  #We assumed DueDate to be 30 days after the invoice date
  dbase.execute('''
    INSERT INTO Invoices(
      InvoiceDate,
      DueDate,
      TotalDueEuro,
      CompanyID)
      VALUES(
        {InvoiceDate},
        DATE({InvoiceDate2},'+30 days'),
        {TotalDueEuro},
        CompanyID)
        '''.format(
          InvoiceDate=str(values_dict['InvoiceDate']),
          InvoiceDate2=str(values_dict['InvoiceDate']),
          TotalDueEuro=TotalDueEuro),
          CompanyID=str(values_dict['CompanyID']))     
  dbase.close()     
  return True

#Check invoices payload example
#{ 
#  "CustomerAccountID": "1"
#}
@app.get("/check_invoices")
async def check_invoices(payload: Request):
  values_dict = await payload.json()
  #open DB
  dbase = sqlite3.connect('database_group43.db', isolation_level=None)
  
  dbase.execute('database_group43.db', isolation_level=None)
  query_invoices = dbase.execute('''
                              SELECT ID FROM Invoices
                              WHERE CustomerAccountID = {CustomerAccountID} AND Paid = 0
                              '''.format(CustomerAccountID=str(values_dict['CustomerAccountID'])))
  invoices_results = query_invoices_status.fetchall()
  dbase.close()
  # Encode results in JSON to send it back as response
  return json.dumps(invoices_results)
  #Customer payment payload example
  #{ 
  #  "InvoiceID": "1",
  #  "CCNumber": "5888 8884 9562 7784"
  #}
@app.post("/customer_payment")
async def customer_paymnent(payload: Request):
  values_dict = await payload.json()
  #open DB
  dbase = sqlite3.connect('database_group43.db', isolation_level=None)
  
  dbase.execute('database_group43.db', isolation_level=None)
  CCNumber = values_dict["CCNumber"]
  query_invoices = dbase.execute('''
                            SELECT ID FROM Invoices
                            WHERE InvoiceID = {InvoiceID} 
                            '''.format(InvoiceID=str(values_dict['InvoiceID'])))
  Invoices_results = query_invoices_status.fetchall()
  #Calculation here
  #validationNumber = 
  # There must be one single invoice with that ID and the validation number must be dividable by 10
  if len(Invoices_results) == 1 and validationNumber % 10 == 0:
    dbase.execute(''' 
      UPDATE Invoice
        SET Paid = 1
        WHERE InvoiceID = {InvoiceID}  
      '''.format(InvoiceID = values_dict['InvoiceID']))
  dbase.close() 
  return True

 #Retrieve statistics payload example
#{ 
# "CompanyID" : "1",
# "Month" : "12",
# "Year" : "2021"
#}
@app.post("/retrieve_statistics")
async def retrieve_statistics(payload: Request):
  values_dict = await payload.json()
  #open DB
  dbase = sqlite3.connect('database_group43.db', isolation_level=None)
  
  dbase.execute('database_group43.db', isolation_level=None)
   # Calculate MRR 
  query_statistics = dbase.execute('''
                              SELECT SUM(TotalDueEuro) 
                              FROM Invoices
                              WHERE CompanyID = {CompanyID} AND strftime('%m',DueDate)={Month} AND strftime('%Y', DueDate)={Year}
                              '''.format(CompanyID=str(values_dict['CompanyID']), Month=str(values_dict['Month']), Year=str(values_dict['Year'])))
  MRR = query_statistics.fetchall()[0][0]
   # Calculate ARR - TO CORRECT !! NOT GOOD
  query_statistics = dbase.execute('''
                              SELECT SUM(TotalDueEuro) 
                              FROM Invoices
                              WHERE CompanyID = {CompanyID} AND strftime('%Y', DueDate)={Year}
                              '''.format(CompanyID=str(values_dict['CompanyID']), Year=str(values_dict['Year'])))
  ARR = query_statistics.fetchall()[0][0]
    #Calculation of number of Customer                                                                                             
  query_Customer = dbase.execute('''
                                  SELECT COUNT(CustomerAccountID) FROM CustomerAccounts
                                  WHERE CompanyID = {CompanyID}'''.format(CompanyID=str(values_dict['CompanyID'])))  

  NumberOfCustomer = query_Customer.fetchall()[0][0]
    #Calculation of average revenue per customer per month
  if NumberOfCustomer > 0:
      query_statistics = dbase.execute('''
                              SELECT SUM(TotalDueEuro) 
                              FROM Invoices
                              WHERE CompanyID = {CompanyID} 
                              '''.format(CompanyID=str(values_dict['CompanyID'])))
      AverageTotalRevenuePerCustomer = query_statistics.fetchall()[0][0] / NumberOfCustomer
  else:
      AverageTotalRevenuePerCustomer = 0
    # Retrieve list of current active subscriptions: Customer name and surname, product name, start and end date
    # All active subscriptions => Active=1 BUT EndDate not passed as we don't have a system to automatically set a subscription as inactive when end date is passed.
  query_Customer = dbase.execute('''
                                  SELECT Name, Surname,ProductName, Subscriptions.StartDate, Subscriptions.EndDate
                                  FROM Subscriptions
                                  LEFT JOIN CustomerAccounts ON CustomerAccounts.ID=Subscriptions.CustomerAccountID
                                  LEFT JOIN Customer ON Customer.ID=CustomerAccounts.CustomerID
                                  LEFT JOIN Products ON Products.ID=Subscriptions.ProductID
                                  WHERE CustomerAccounts.CompanyID={CompanyID} 
                                    AND Subscriptions.Active=1 
                                    AND Subscriptions.EndDate >= date('now')'''.format(CompanyID=str(values_dict['CompanyID'])))
  active_subscriptions_results = query_Customer.fetchall()
    # return json.dumps(active_subscriptions_results

  return True








if __name__ == '__main__':
  uvicorn.run(app, host='127.0.0.1', port=8000)
