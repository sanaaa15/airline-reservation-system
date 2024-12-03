
import streamlit as st
from amadeus import Client, ResponseError

amadeus = Client(
    client_id="gwZTRzthoJkGJIlQPB77rtY8Po2cXROo",
    client_secret="3n2GsjM62jU7FZT1"
)


def search_flights(origin, destination, departure_date, currency, cabin_class, traveler_type):
    try:
        response = amadeus.shopping.flight_offers_search.post(
            {
                "currencyCode": currency,
                "originDestinations": [
                    {
                        "id": "1",
                        "originLocationCode": origin,
                        "destinationLocationCode": destination,
                        "departureDateTimeRange": {
                            "date": departure_date,
                            "time": "10:00:00"
                        }
                    }
                ],
                "travelers": [
                    {
                        "id": "1",
                        "travelerType": traveler_type
                    }
                ],
                "sources": ["GDS"],
                "searchCriteria": {
                    "maxFlightOffers": 5,  
                    "flightFilters": {
                        "cabinRestrictions": [
                            {
                                "cabin": cabin_class,
                                "coverage": "MOST_SEGMENTS",
                                "originDestinationIds": ["1"]
                            }
                        ]
                    }
                }
            }
        )
        results = response.data

        
        if results:
            flights = [
                f"Flight from {flight['itineraries'][0]['segments'][0]['departure']['iataCode']} "
                f"to {flight['itineraries'][0]['segments'][0]['arrival']['iataCode']} "
                f"for {flight['price']['total']} {currency}"
                for flight in results
            ]
            return "\n".join(flights)
        else:
            return "No flights found for the provided details."
    except ResponseError as error:
        return f"Error: {error}"


st.title("Airline Reservation Chatbot")
st.image("https://t4.ftcdn.net/jpg/06/52/07/61/360_F_652076107_GlysMpUCLf6Gx5rgf2Y4W3MqVXMvz7D0.jpg")
st.write("Welcome to the Airline Reservation Chatbot! Please provide your details below.")

st.subheader("Search Flights")
origin = st.text_input("Origin (IATA Code):", placeholder="E.g., NYC")
destination = st.text_input("Destination (IATA Code):", placeholder="E.g., MAD")
departure_date = st.date_input("Departure Date:")
currency = st.text_input("Currency Code:", value="USD", placeholder="E.g., USD")
cabin_class = st.selectbox("Cabin Class:", ["ECONOMY", "PREMIUM_ECONOMY", "BUSINESS", "FIRST"])
traveler_type = st.selectbox("Traveler Type:", ["ADULT", "CHILD", "INFANT"])

if st.button("Search Flights"):
    if origin and destination and departure_date and currency and cabin_class and traveler_type:
        flights = search_flights(origin, destination, departure_date.isoformat(), currency, cabin_class, traveler_type)
        st.text_area("Available Flights:", flights, height=300)
    else:
        st.error("Please fill in all fields.")