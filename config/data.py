import streamlit as st
from simple_salesforce import Salesforce
import config.connections as con
import pandas as pd

## CONNECTIONS
sf = con.get_salesforce()
supa = con.get_supabase()

## SUPABASE


### SALESFORCE
def get_sf_query(varObject, filterCriteria=None):
    # Define fields for each object
    fields_dict = {
        "Opportunity": "Id, Name, AccountId, Account.Name, OwnerId, Owner.Name, ContractId, CreatedDate, Created_From_Asset_or_Contract__c, CloseDate, Amount, Amount__c, Email__c, Install_Date__c, Type, Product__c, Pricebook2Id, RecordTypeId, RecordType.Name, Sales_Rep__c, StageName, Subsidiary__c, Territory2Id, Delivery_Date__c",
        "Contract": "Id, AccountId, Account.Name, StartDate, EndDate, BillingStreet, BillingCity, BillingState, BillingPostalCode, BillingCountry, BillingStateCode, BillingCountryCode, BillingLatitude, BillingLongitude, BillingGeocodeAccuracy, BillingAddress, ShippingStreet, ShippingCity, ShippingState, ShippingPostalCode, ShippingCountry, ShippingStateCode, ShippingCountryCode, ShippingLatitude, ShippingLongitude, ShippingGeocodeAccuracy, ShippingAddress, ContractTerm, OwnerId, Owner.Name, Status, Asset__c, Serial_Number__c, BP__c, Product_Name__c, Sales_Order__c, Contract_Price__c, Type__c, Opportunity_Opend__c, Product__c, Subsidiary__c",
        "User": "Id, Username, LastName, FirstName, Name, Email"
    }

    # Get fields for the specified object
    varQueryFields = fields_dict.get(varObject, "")

    # Constructing the SOQL query
    query = f"SELECT {varQueryFields} FROM {varObject}"
    if filterCriteria:
        filter_strings = [f"{field} = '{value}'" for field, value in filterCriteria.items()]
        query += " WHERE " + " AND ".join(filter_strings)

    return query


def create_df_sfdc(varQuery):
  
  data = sf.query(varQuery)
  records = data['records']
   
  if not records:
      return pd.DataFrame()
   
  columns = records[0].keys()
  df = pd.DataFrame(columns=columns)

  for record in records:
    df = df.append(record, ignore_index=True)

  return df

def get_sfdc_data(varType):
  if varType=="User":
     query = get_sf_query("User", {"Subsidiary__c": "Alma Lasers , Inc."})
     df = create_df_sfdc(query)
     
  elif varType=="Opportunity":
     query = get_sf_query("Opportunity", {"Subsidiary__c": "Alma Lasers , Inc.", "OwnerId": st.session_state.sfid})
     df = create_df_sfdc(query)

  elif varType=="Contract":
     query = get_sf_query("Contract", {"Subsidiary__c": "Alma Lasers , Inc."})
     df = create_df_sfdc(query)
  
  else:
     query = get_sf_query("Opportunity", {"Subsidiary__c": "Alma Lasers , Inc.", "OwnerId": st.session_state.sfid}) 
     
  df = create_df_sfdc(query)
  return df

@st.cache_data
def get_data_salesforce_all():
    dfOpps = get_sfdc_data("Opportunity")
    dfUser = get_sfdc_data("User")
    dfContract = get_sfdc_data("Contract")

    st.session_state.dfOpps = dfOpps
    st.session_state.dfUsers = dfUser
    st.session_state.dfContracts = dfContract
    st.session_state.data_loaded = True
    
    return dfOpps, dfUser, dfContract