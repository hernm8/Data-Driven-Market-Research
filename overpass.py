import requests
import folium
from folium.plugins import MarkerCluster
import webbrowser

# Function to fetch data from Overpass API
def get_overpass_data(city):
    query = f"""
    [out:json][timeout:25];
    // fetch area by the name "{city}"
    area["name"="{city}"]->.searchArea;
    // gather results for schools, hospitals, clinics, and restaurants
    (
      node["amenity"="school"](area.searchArea);
      node["amenity"="hospital"](area.searchArea);
      node["amenity"="clinic"](area.searchArea);
      node["amenity"="restaurant"](area.searchArea);
    );
    out body;
    """
    
    url = "https://overpass-api.de/api/interpreter"

    print(f"Sending request to Overpass API for {city}...")
    try:
        response = requests.get(url, params={'data': query})
        response.raise_for_status()
        print("Request successful, processing data...")

        data = response.json()

        if data['elements']:
            print(f"Found {len(data['elements'])} results.")
            return data['elements']
        else:
            print("No results found.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

# Function to create map with amenities
def create_map(data, city_name):
    # Create a base map centered around the city
    map_center = [41.7637, -72.6851]  # Default to Hartford, CT coordinates
    my_map = folium.Map(location=map_center, zoom_start=13)

    # Create a marker cluster to group markers
    marker_cluster = MarkerCluster().add_to(my_map)
    
    # Loop through the data and add markers for each amenity
    for element in data:
        lat = element.get('lat')
        lon = element.get('lon')
        amenity = element.get('tags', {}).get('amenity', 'Unknown')
        
        if lat and lon:
            folium.Marker([lat, lon], popup=amenity).add_to(marker_cluster)

    # Save the map as an HTML file
    map_file = f"{city_name}_amenities_map.html"
    my_map.save(map_file)
    print(f"Map saved as {map_file}")

    # Open the map in the web browser automatically
    webbrowser.open(map_file)

# Example usage
city_name = "Hartford"
data = get_overpass_data(city_name)

if data:
    create_map(data, city_name)
else:
    print("No data to visualize.")
