from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- Core Data Structure (All prices are in INR - Indian Rupees) ---
# Total of 27 comprehensive builds, covering budgets from 20K up to 400K.
BUILD_DATA = [
    # ---------------------------------- General Use Builds (4) ----------------------------------
    {
        "name": "Tier 0: Essential Web & Doc Build",
        "price": 20000, 
        "purpose": "general",
        "components": {
            "CPU": "Intel Celeron/Older i3 (Dual Core)",
            "GPU": "Integrated Intel HD Graphics (Basic)",
            "RAM": "8GB DDR4 (1x8GB) 2400MHz",
            "Storage": "128GB SATA SSD",
            "Motherboard": "H310/A320 Micro ATX",
            "PSU": "300W Standard",
            "Case": "Ultra-Slim/Used Case"
        }
    },
    {
        "name": "Tier 1: Ultra-Budget Daily Driver",
        "price": 25000, 
        "purpose": "general",
        "components": {
            "CPU": "Intel Core i3-10100 (Integrated Graphics)",
            "GPU": "Integrated Intel UHD Graphics",
            "RAM": "8GB DDR4 (1x8GB) 2666MHz",
            "Storage": "256GB SATA SSD",
            "Motherboard": "H510 Micro ATX",
            "PSU": "350W 80+ Standard",
            "Case": "Basic Slim Tower"
        }
    },
    {
        "name": "Tier 2: Budget Plus Daily Driver APU",
        "price": 30000, 
        "purpose": "general",
        "components": {
            "CPU": "AMD Ryzen 5 5600G (Integrated Graphics)",
            "GPU": "Integrated Vega 7 Graphics (Great for Daily Use)",
            "RAM": "16GB DDR4 (2x8GB) 3200MHz (Crucial for APU)",
            "Storage": "500GB NVMe SSD",
            "Motherboard": "A520 Micro ATX",
            "PSU": "450W 80+ White",
            "Case": "Simple MicroATX Tower"
        }
    },
    {
        "name": "Tier 3: Basic Value Workstation",
        "price": 40050, 
        "purpose": "general",
        "components": {
            "CPU": "Intel Core i5-12400 (Integrated Graphics)",
            "GPU": "Integrated Intel UHD 730 Graphics",
            "RAM": "16GB DDR4 (2x8GB) 3200MHz",
            "Storage": "1TB NVMe SSD",
            "Motherboard": "B660 Micro ATX",
            "PSU": "550W 80+ Bronze",
            "Case": "Simple Mid-Tower"
        }
    },

    # ------------------------------------ Gaming Builds (12 Total) -------------------------------------
    {
        "name": "Gaming Tier 0.5: Absolute Entry 720p/Light Esports",
        "price": 35000,
        "purpose": "gaming",
        "components": {
            "CPU": "AMD Ryzen 3 3200G/Intel i3-10100F",
            "GPU": "Used GTX 1050Ti 4GB / RX 570 4GB (Priority)",
            "RAM": "8GB DDR4 (2x4GB) 3000MHz",
            "Storage": "500GB NVMe SSD",
            "Motherboard": "A320/H410 Micro ATX",
            "PSU": "450W Standard",
            "Case": "Budget MicroATX Tower"
        }
    },
    {
        "name": "Gaming Tier 1: Entry Level 1080p (Value)",
        "price": 50000,
        "purpose": "gaming",
        "components": {
            "CPU": "AMD Ryzen 5 5500",
            "GPU": "AMD Radeon RX 6600 8GB (High Priority)",
            "RAM": "16GB DDR4 (2x8GB) 3200MHz",
            "Storage": "500GB NVMe SSD",
            "Motherboard": "B450/B550 Micro ATX",
            "PSU": "550W 80+ Bronze",
            "Case": "Compact Mesh Case"
        }
    },
    {
        "name": "Gaming Tier 2: Solid 1080p Maxed",
        "price": 65000,
        "purpose": "gaming",
        "components": {
            "CPU": "AMD Ryzen 5 5600",
            "GPU": "NVIDIA RTX 3060 8GB",
            "RAM": "16GB DDR4 (2x8GB) 3600MHz",
            "Storage": "1TB NVMe SSD",
            "Motherboard": "B550 ATX",
            "PSU": "650W 80+ Bronze",
            "Case": "Mid-Tower Mesh Case"
        }
    },
    {
        "name": "Gaming Tier 3: High Refresh 1080p / Entry 1440p",
        "price": 85000,
        "purpose": "gaming",
        "components": {
            "CPU": "Intel Core i5-13400F",
            "GPU": "AMD Radeon RX 7600 XT 16GB (VRAM Focus)",
            "RAM": "32GB DDR4 (2x16GB) 3600MHz",
            "Storage": "1TB NVMe Gen4 SSD",
            "Motherboard": "B760 ATX",
            "PSU": "750W 80+ Gold",
            "Case": "High Airflow Mid-Tower"
        }
    },
    {
        "name": "Gaming Tier 4: Mid-Range 1440p Specialist",
        "price": 105000,
        "purpose": "gaming",
        "components": {
            "CPU": "Intel Core i5-13600K",
            "GPU": "AMD Radeon RX 7800 XT 16GB",
            "RAM": "32GB DDR5 (2x16GB) 6000MHz",
            "Storage": "2TB NVMe SSD",
            "Motherboard": "Z790 ATX",
            "PSU": "850W 80+ Gold Modular",
            "Case": "Premium Mid-Tower (Good Airflow)"
        }
    },
    {
        "name": "Gaming Tier 5: High-End 1440p / Entry 4K",
        "price": 130000,
        "purpose": "gaming",
        "components": {
            "CPU": "AMD Ryzen 7 7700X",
            "GPU": "NVIDIA RTX 4070 SUPER 12GB (DLSS/RT Focus)",
            "RAM": "32GB DDR5 (2x16GB) 6000MHz",
            "Storage": "2TB NVMe Gen4 SSD",
            "Motherboard": "X670 ATX",
            "PSU": "850W 80+ Platinum Modular",
            "Case": "High-End Mid-Tower"
        }
    },
    {
        "name": "Gaming Tier 6: True 4K Specialist",
        "price": 160000,
        "purpose": "gaming",
        "components": {
            "CPU": "Intel Core i7-14700K",
            "GPU": "NVIDIA RTX 4070 Ti SUPER 16GB",
            "RAM": "64GB DDR5 (2x32GB) 6400MHz",
            "Storage": "4TB NVMe Gen4 SSD",
            "Motherboard": "Z790 ATX (Premium)",
            "PSU": "1000W 80+ Gold ATX 3.0",
            "Case": "Premium Full Tower (Silent Focus)"
        }
    },
    {
        "name": "Gaming Tier 7: Maxed Out 4K/Competitive",
        "price": 200000,
        "purpose": "gaming",
        "components": {
            "CPU": "AMD Ryzen 9 7900X3D",
            "GPU": "AMD Radeon RX 7900 XTX 24GB (Raw Power)",
            "RAM": "64GB DDR5 (2x32GB) 6400MHz",
            "Storage": "4TB NVMe Gen4 SSD + 4TB NVMe Gen4 SSD",
            "Motherboard": "X670E ATX",
            "PSU": "1200W 80+ Platinum",
            "Case": "High-Airflow Full Tower"
        }
    },
    {
        "name": "Gaming Tier 8: Extreme Ray Tracing Enthusiast",
        "price": 240000,
        "purpose": "gaming",
        "components": {
            "CPU": "Intel Core i9-14900K",
            "GPU": "NVIDIA RTX 4080 SUPER 16GB",
            "RAM": "64GB DDR5 (2x32GB) 7200MHz (High Speed)",
            "Storage": "4TB NVMe Gen4 SSD",
            "Motherboard": "Z790 ATX (High-End VRMs)",
            "PSU": "1200W 80+ Platinum ATX 3.0",
            "Case": "AIO Ready Mid-Tower"
        }
    },
    {
        "name": "Gaming Tier 9: Absolute Flagship",
        "price": 300000,
        "purpose": "gaming",
        "components": {
            "CPU": "AMD Ryzen 9 7950X3D (Max Cache)",
            "GPU": "NVIDIA RTX 4090 24GB (Max Priority)",
            "RAM": "64GB DDR5 (2x32GB) 6400MHz (Low Latency)",
            "Storage": "4TB NVMe Gen4 SSD + 4TB NVMe Gen5 SSD (Future Proof)",
            "Motherboard": "X670E ATX (Flagship)",
            "PSU": "1600W 80+ Titanium ATX 3.0",
            "Case": "Custom Loop Ready Full Tower"
        }
    },
    {
        "name": "Gaming Tier 10: Showcase/Custom Loop Dream",
        "price": 320000,
        "purpose": "gaming",
        "components": {
            "CPU": "Intel Core i9-14900K (Overclock Ready)",
            "GPU": "NVIDIA RTX 4090 24GB (Liquid Cooled Variant)",
            "RAM": "64GB DDR5 (2x32GB) 7200MHz",
            "Storage": "8TB NVMe Gen4 SSD",
            "Motherboard": "Z790 (Aesthetics Focused)",
            "PSU": "1300W 80+ Platinum ATX 3.0",
            "Case": "Open-Frame or Panoramic Full Tower"
        }
    },
    {
        "name": "Gaming Tier 11: Ultimate Performance & Aesthetics",
        "price": 350000,
        "purpose": "gaming",
        "components": {
            "CPU": "AMD Ryzen 9 9950X (Simulated Future CPU)",
            "GPU": "NVIDIA RTX 4090 24GB (Best Available)",
            "RAM": "128GB DDR5 (4x32GB) 6000MHz (Future Proof)",
            "Storage": "8TB NVMe Gen4 SSD (RAID 0)",
            "Motherboard": "X870E ATX (Simulated)",
            "PSU": "1600W 80+ Titanium",
            "Case": "Maximum Customization Full Tower"
        }
    },

    # --------------------------------- Productivity Builds (9 Total) ----------------------------------
    {
        "name": "Prod Tier 0: Budget Developer/Content Starter",
        "price": 50000,
        "purpose": "productivity",
        "components": {
            "CPU": "Intel Core i5-13400 (Good Value Cores)",
            "GPU": "Basic GTX 1650 4GB / RTX 3050 6GB", 
            "RAM": "16GB DDR4 (2x8GB) 3200MHz",
            "Storage": "1TB NVMe SSD",
            "Motherboard": "B660 Micro ATX",
            "PSU": "550W 80+ Bronze",
            "Case": "Quiet Mid-Tower"
        }
    },
    {
        "name": "Prod Tier 1: Productivity Starter Build",
        "price": 75000,
        "purpose": "productivity",
        "components": {
            "CPU": "Intel Core i5-14400F",
            "GPU": "NVIDIA RTX 4060 8GB (Good Encoder)", 
            "RAM": "32GB DDR4 (2x16GB) 3200MHz (High Priority)",
            "Storage": "1TB NVMe SSD + 2TB HDD",
            "Motherboard": "B760 ATX",
            "PSU": "650W 80+ Gold",
            "Case": "Quiet Mid-Tower"
        }
    },
    {
        "name": "Prod Tier 2: Pro Creator / Mid-Range A/V",
        "price": 110000,
        "purpose": "productivity",
        "components": {
            "CPU": "AMD Ryzen 9 7900 (High Cores/Threads)",
            "GPU": "NVIDIA RTX 4060 Ti 16GB (VRAM Focus)", 
            "RAM": "64GB DDR5 (2x32GB) 6000MHz (Max Priority)",
            "Storage": "2TB NVMe Gen4 SSD + 4TB HDD",
            "Motherboard": "X670 ATX",
            "PSU": "850W 80+ Gold Modular",
            "Case": "Silent & High-Airflow Full-Tower"
        }
    },
    {
        "name": "Prod Tier 3: Professional Video Editing Specialist",
        "price": 140000,
        "purpose": "productivity",
        "components": {
            "CPU": "Intel Core i7-14700F (High Core Count)",
            "GPU": "NVIDIA RTX 4070 12GB (VRAM Focus)", 
            "RAM": "64GB DDR5 (2x32GB) 6000MHz",
            "Storage": "4TB NVMe Gen4 SSD (Fast Storage)",
            "Motherboard": "B760 ATX (High Capacity)",
            "PSU": "850W 80+ Gold",
            "Case": "Sound Dampened Tower"
        }
    },
    {
        "name": "Prod Tier 4: AI/CAD/ML Workstation",
        "price": 200000,
        "purpose": "productivity",
        "components": {
            "CPU": "AMD Ryzen 9 7950X3D (Max Cores/Cache)",
            "GPU": "NVIDIA RTX 4080 SUPER 16GB (VRAM/Cuda)", 
            "RAM": "128GB DDR5 (4x32GB) 6000MHz (Max RAM)",
            "Storage": "4TB NVMe Gen4 SSD + 8TB External Backup",
            "Motherboard": "X670E ATX (High Feature Set)",
            "PSU": "1000W 80+ Platinum",
            "Case": "Large High-Airflow Workstation"
        }
    },
    {
        "name": "Prod Tier 5: Data Science / Virtualization",
        "price": 250000,
        "purpose": "productivity",
        "components": {
            "CPU": "Intel Core i9-14900K (Raw Core Power)",
            "GPU": "NVIDIA RTX 4090 24GB (VRAM King)", 
            "RAM": "128GB DDR5 (4x32GB) 6400MHz",
            "Storage": "8TB NVMe Gen4 SSD (RAID Setup)",
            "Motherboard": "Z790 ATX (High VRM)",
            "PSU": "1200W 80+ Platinum ATX 3.0",
            "Case": "Optimized Cooling Tower"
        }
    },
    # ------------------------------------- Hybrid Builds (4 Total) ------------------------------------
    {
        "name": "Hybrid Prosumer 1: Balanced Gaming/Work",
        "price": 160000,
        "purpose": "hybrid",
        "components": {
            "CPU": "Intel Core i7-14700K (Gaming & Multitasking)",
            "GPU": "NVIDIA RTX 4070 Ti SUPER 16GB", 
            "RAM": "64GB DDR5 (2x32GB) 6000MHz",
            "Storage": "4TB NVMe Gen4 SSD",
            "Motherboard": "Z790 ATX",
            "PSU": "1000W 80+ Gold Modular",
            "Case": "Premium Mid-Tower (Silent/Airflow Balance)"
        }
    },
    {
        "name": "Hybrid Prosumer 2: High-End Creator/4K Gaming",
        "price": 220000,
        "purpose": "hybrid",
        "components": {
            "CPU": "AMD Ryzen 9 7950X",
            "GPU": "NVIDIA RTX 4080 SUPER 16GB", 
            "RAM": "128GB DDR5 (4x32GB) 6000MHz",
            "Storage": "8TB NVMe Gen4 SSD",
            "Motherboard": "X670E ATX",
            "PSU": "1200W 80+ Platinum",
            "Case": "Full-Tower Workstation/Gaming"
        }
    },
    {
        "name": "Hybrid Prosumer 3: Extreme Workstation/Gaming",
        "price": 300000,
        "purpose": "hybrid",
        "components": {
            "CPU": "Intel Core i9-14900K",
            "GPU": "NVIDIA RTX 4090 24GB", 
            "RAM": "128GB DDR5 (4x32GB) 7200MHz",
            "Storage": "8TB NVMe Gen5 SSD",
            "Motherboard": "Z790 ATX (Maxed Out)",
            "PSU": "1600W 80+ Titanium ATX 3.0",
            "Case": "Showcase Full Tower"
        }
    },
    {
        "name": "Hybrid Prosumer 4: Ultimate Multi-Core/Pro Focus",
        "price": 400000,
        "purpose": "hybrid",
        "components": {
            "CPU": "AMD Ryzen Threadripper PRO 5955WX (Simulated)",
            "GPU": "NVIDIA RTX A6000 48GB (Pro VRAM Focus)",
            "RAM": "256GB ECC DDR4 (8x32GB) (Max Stability)",
            "Storage": "16TB NVMe Gen4 (RAID Setup)",
            "Motherboard": "WRX80 Workstation",
            "PSU": "2000W 80+ Titanium",
            "Case": "Server/Workstation Full Tower (Max Cooling)"
        }
    },
]

# --- Core Logic Function ---
def find_best_build(budget, purpose='general'):
    """
    Finds the highest-priced PC build that is less than or equal to the given budget,
    optionally filtered by a specific purpose.
    """
    best_match = None
    highest_price_found = -1

    # Define the filtering rules
    if purpose == 'general':
        # General purpose checks all builds
        filtered_builds = BUILD_DATA
    elif purpose == 'hybrid':
        # Hybrid purpose checks both dedicated 'hybrid' and all 'productivity' and 'gaming' builds for flexibility
        filtered_builds = [
            data for data in BUILD_DATA 
            if data['purpose'] in ['hybrid', 'productivity', 'gaming']
        ]
    else:
        # Filter only by the specific purpose (gaming or productivity)
        filtered_builds = [data for data in BUILD_DATA if data['purpose'] == purpose]

    for data in filtered_builds:
        build_price = data['price']
        if build_price <= budget and build_price > highest_price_found:
            highest_price_found = build_price
            best_match = data

    return best_match


@app.route('/')
def index():
    """Serves the main HTML page. Assumes index.html is in the 'templates' folder."""
    return render_template('index.html')


@app.route('/api/get_build', methods=['POST'])
def get_build():
    """
    API endpoint to receive budget and purpose, run the Python logic, and return JSON.
    """
    try:
        data = request.get_json()
        budget = int(data.get('budget'))
        purpose = data.get('purpose', 'general')

        if budget is None or budget <= 0:
            return jsonify({
                "success": False, 
                "message": "Invalid budget provided."
            }), 400

        # Run the core Python logic
        result_data = find_best_build(budget, purpose)

        if result_data:
            # Calculate remaining budget and send everything back
            remaining_budget = budget - result_data['price']
            
            # Use JSON response for success
            return jsonify({
                "success": True,
                "build": result_data,
                "remaining_budget": remaining_budget
            })
        else:
            # Handle case where no build is found
            
            # Determine which builds to consider for finding the minimum price based on purpose
            if purpose == 'general':
                purpose_builds = [d for d in BUILD_DATA if d['purpose'] == 'general']
            elif purpose == 'hybrid':
                purpose_builds = [d for d in BUILD_DATA if d['purpose'] in ['hybrid', 'productivity', 'gaming']]
            else:
                purpose_builds = [d for d in BUILD_DATA if d['purpose'] == purpose]

            # Find the minimum price among the relevant builds
            min_price = min([d['price'] for d in purpose_builds]) if purpose_builds else None
            
            message = "No PC build found within your budget."
            if min_price is not None:
                # Format price with commas for readability
                message += f" The minimum price for a suitable build is ₹{min_price:,}."

            return jsonify({
                "success": False,
                "message": message
            }), 404

    except ValueError:
        return jsonify({
            "success": False,
            "message": "Budget must be a valid number."
        }), 400
    except Exception as e:
        # Catch unexpected errors
        app.logger.error(f"Error processing request: {e}")
        return jsonify({
            "success": False,
            "message": f"An unexpected error occurred: {str(e)}"
        }), 500

if __name__ == '__main__':
    # Running in debug mode for local development
    app.run(debug=True)

    