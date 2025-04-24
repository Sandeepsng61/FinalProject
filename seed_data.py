import os
import sys
from datetime import datetime
from app import db
from models import User, Product
from werkzeug.security import generate_password_hash

def create_admin_user():
    # Check if admin user exists
    admin = User.query.filter_by(email="admin@example.com").first()
    if not admin:
        # Create admin user
        admin = User(
            username="admin",
            email="admin@example.com",
            password_hash=generate_password_hash("admin123"),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created.")
    else:
        print("Admin user already exists.")

def create_test_user():
    # Check if test user exists
    test_user = User.query.filter_by(email="user@example.com").first()
    if not test_user:
        # Create test user
        test_user = User(
            username="testuser",
            email="user@example.com",
            password_hash=generate_password_hash("user123"),
            is_admin=False
        )
        db.session.add(test_user)
        db.session.commit()
        print("Test user created.")
    else:
        print("Test user already exists.")

def create_products():
    # Check if products exist
    products_count = Product.query.count()
    if products_count > 0:
        print(f"{products_count} products already exist.")
        choice = input("Do you want to clear existing products and create new ones? (y/n): ")
        if choice.lower() != 'y':
            return
        # Clear existing products
        Product.query.delete()
        db.session.commit()
        print("Existing products deleted.")
    
    # CPU products
    cpus = [
        {
            "name": "Intel Core i9-12900K",
            "description": "Intel's flagship 12th Gen desktop processor with 16 cores and 24 threads.",
            "price": 59999.00,
            "category": "cpu",
            "image_url": "https://m.media-amazon.com/images/I/61aMf-HuJKL._AC_SL1500_.jpg",
            "stock": 15,
            "specs": {
                "cores": 16,
                "threads": 24,
                "base_frequency": "3.2 GHz",
                "boost_frequency": "5.2 GHz",
                "cache": "30 MB",
                "tdp": "125W",
                "socket": "LGA 1700",
                "architecture": "Alder Lake"
            }
        },
        {
            "name": "AMD Ryzen 9 5950X",
            "description": "AMD's high-performance processor with 16 cores and 32 threads for enthusiasts and creators.",
            "price": 54999.00,
            "category": "cpu",
            "image_url": "https://m.media-amazon.com/images/I/616VM20+AzL._AC_SL1384_.jpg",
            "stock": 12,
            "specs": {
                "cores": 16,
                "threads": 32,
                "base_frequency": "3.4 GHz",
                "boost_frequency": "4.9 GHz",
                "cache": "72 MB",
                "tdp": "105W",
                "socket": "AM4",
                "architecture": "Zen 3"
            }
        },
        {
            "name": "Intel Core i7-12700K",
            "description": "12th Generation Intel Core i7 processor for gaming and productivity with 12 cores and 20 threads.",
            "price": 44999.00,
            "category": "cpu",
            "image_url": "https://m.media-amazon.com/images/I/71CVbGGcrVL._AC_SL1500_.jpg",
            "stock": 20,
            "specs": {
                "cores": 12,
                "threads": 20,
                "base_frequency": "3.6 GHz",
                "boost_frequency": "5.0 GHz",
                "cache": "25 MB",
                "tdp": "125W",
                "socket": "LGA 1700",
                "architecture": "Alder Lake"
            }
        },
        {
            "name": "AMD Ryzen 7 5800X",
            "description": "8-core, 16-thread processor for high-performance gaming and content creation.",
            "price": 34999.00,
            "category": "cpu",
            "image_url": "https://m.media-amazon.com/images/I/61IIbwz-+ML._AC_SL1500_.jpg",
            "stock": 18,
            "specs": {
                "cores": 8,
                "threads": 16,
                "base_frequency": "3.8 GHz",
                "boost_frequency": "4.7 GHz",
                "cache": "36 MB",
                "tdp": "105W",
                "socket": "AM4",
                "architecture": "Zen 3"
            }
        }
    ]
    
    # Motherboard products
    motherboards = [
        {
            "name": "ASUS ROG Maximus Z690 Hero",
            "description": "Premium Z690 motherboard for Intel 12th Gen processors with advanced features and overclocking capabilities.",
            "price": 62999.00,
            "category": "motherboard",
            "image_url": "https://m.media-amazon.com/images/I/81oJ+hibBgL._AC_SL1500_.jpg",
            "stock": 8,
            "specs": {
                "chipset": "Z690",
                "socket": "LGA 1700",
                "form_factor": "ATX",
                "memory_slots": 4,
                "max_memory": "128 GB",
                "pcie_slots": "PCI-E 5.0 x16, PCI-E 4.0 x16",
                "m2_slots": 5,
                "wifi": "Wi-Fi 6E",
                "rgb": "Aura Sync RGB"
            }
        },
        {
            "name": "MSI MAG B550 TOMAHAWK",
            "description": "Feature-rich B550 motherboard with excellent VRM for AMD Ryzen 5000 series processors.",
            "price": 18999.00,
            "category": "motherboard",
            "image_url": "https://m.media-amazon.com/images/I/91ntjHXUuBL._AC_SL1500_.jpg",
            "stock": 15,
            "specs": {
                "chipset": "B550",
                "socket": "AM4",
                "form_factor": "ATX",
                "memory_slots": 4,
                "max_memory": "128 GB",
                "pcie_slots": "PCI-E 4.0 x16, PCI-E 3.0 x16",
                "m2_slots": 2,
                "wifi": "None",
                "rgb": "Mystic Light RGB"
            }
        },
        {
            "name": "ASUS TUF Gaming B660M-PLUS WiFi",
            "description": "Durable micro-ATX motherboard with Wi-Fi 6 for Intel 12th Gen processors.",
            "price": 17499.00,
            "category": "motherboard",
            "image_url": "https://m.media-amazon.com/images/I/91Q633RYkML._AC_SL1500_.jpg",
            "stock": 22,
            "specs": {
                "chipset": "B660",
                "socket": "LGA 1700",
                "form_factor": "Micro-ATX",
                "memory_slots": 4,
                "max_memory": "128 GB",
                "pcie_slots": "PCI-E 4.0 x16, PCI-E 3.0 x16",
                "m2_slots": 2,
                "wifi": "Wi-Fi 6",
                "rgb": "Aura Sync RGB"
            }
        },
        {
            "name": "GIGABYTE X570 AORUS ELITE",
            "description": "High-performance X570 motherboard with premium features for AMD Ryzen processors.",
            "price": 24999.00,
            "category": "motherboard",
            "image_url": "https://m.media-amazon.com/images/I/819MWPQ3bBL._AC_SL1500_.jpg",
            "stock": 10,
            "specs": {
                "chipset": "X570",
                "socket": "AM4",
                "form_factor": "ATX",
                "memory_slots": 4,
                "max_memory": "128 GB",
                "pcie_slots": "PCI-E 4.0 x16, PCI-E 4.0 x8",
                "m2_slots": 3,
                "wifi": "None",
                "rgb": "RGB Fusion 2.0"
            }
        }
    ]
    
    # GPU products
    gpus = [
        {
            "name": "NVIDIA GeForce RTX 3080 Ti",
            "description": "High-end graphics card for 4K gaming and creative work with ray tracing and DLSS capabilities.",
            "price": 124999.00,
            "category": "gpu",
            "image_url": "https://m.media-amazon.com/images/I/81+gdlgzctL._AC_SL1500_.jpg",
            "stock": 7,
            "specs": {
                "memory": "12GB GDDR6X",
                "cuda_cores": 10240,
                "boost_clock": "1.67 GHz",
                "memory_interface": "384-bit",
                "power_consumption": "350W",
                "ports": "HDMI 2.1, DisplayPort 1.4a",
                "ray_tracing": "2nd Generation",
                "tensor_cores": "3rd Generation"
            }
        },
        {
            "name": "AMD Radeon RX 6800 XT",
            "description": "High-performance graphics card with 16GB VRAM for gaming and content creation.",
            "price": 89999.00,
            "category": "gpu",
            "image_url": "https://m.media-amazon.com/images/I/81rQEYcPcpL._AC_SL1500_.jpg",
            "stock": 9,
            "specs": {
                "memory": "16GB GDDR6",
                "stream_processors": 4608,
                "boost_clock": "2.25 GHz",
                "memory_interface": "256-bit",
                "power_consumption": "300W",
                "ports": "HDMI 2.1, DisplayPort 1.4",
                "ray_tracing": "Yes",
                "infinity_cache": "128MB"
            }
        },
        {
            "name": "NVIDIA GeForce RTX 3070",
            "description": "Excellent 1440p gaming performance with ray tracing and DLSS support.",
            "price": 69999.00,
            "category": "gpu",
            "image_url": "https://m.media-amazon.com/images/I/81QXSV7vJsL._AC_SL1500_.jpg",
            "stock": 12,
            "specs": {
                "memory": "8GB GDDR6",
                "cuda_cores": 5888,
                "boost_clock": "1.73 GHz",
                "memory_interface": "256-bit",
                "power_consumption": "220W",
                "ports": "HDMI 2.1, DisplayPort 1.4a",
                "ray_tracing": "2nd Generation",
                "tensor_cores": "3rd Generation"
            }
        },
        {
            "name": "AMD Radeon RX 6700 XT",
            "description": "Great 1440p gaming performance with 12GB VRAM at a competitive price.",
            "price": 54999.00,
            "category": "gpu",
            "image_url": "https://m.media-amazon.com/images/I/81vDZyJQ-4L._AC_SL1500_.jpg",
            "stock": 15,
            "specs": {
                "memory": "12GB GDDR6",
                "stream_processors": 2560,
                "boost_clock": "2.58 GHz",
                "memory_interface": "192-bit",
                "power_consumption": "230W",
                "ports": "HDMI 2.1, DisplayPort 1.4",
                "ray_tracing": "Yes",
                "infinity_cache": "96MB"
            }
        }
    ]
    
    # RAM products
    rams = [
        {
            "name": "Corsair Vengeance RGB Pro 32GB",
            "description": "High-performance RGB memory kit for gaming and content creation.",
            "price": 18999.00,
            "category": "ram",
            "image_url": "https://m.media-amazon.com/images/I/71-mz8xkfKL._AC_SL1500_.jpg",
            "stock": 25,
            "specs": {
                "capacity": "32GB (2x16GB)",
                "speed": "3600MHz",
                "type": "DDR4",
                "cas_latency": "18",
                "voltage": "1.35V",
                "rgb": "Yes",
                "heat_spreader": "Aluminum",
                "xmp_profiles": "Yes"
            }
        },
        {
            "name": "G.SKILL Trident Z RGB 16GB",
            "description": "RGB memory kit with excellent performance and compatibility.",
            "price": 12999.00,
            "category": "ram",
            "image_url": "https://m.media-amazon.com/images/I/61a90IXJJDL._AC_SL1500_.jpg",
            "stock": 30,
            "specs": {
                "capacity": "16GB (2x8GB)",
                "speed": "3200MHz",
                "type": "DDR4",
                "cas_latency": "16",
                "voltage": "1.35V",
                "rgb": "Yes",
                "heat_spreader": "Aluminum",
                "xmp_profiles": "Yes"
            }
        },
        {
            "name": "Kingston FURY Beast 32GB",
            "description": "High-performance memory kit with stylish heat spreaders and stability.",
            "price": 16999.00,
            "category": "ram",
            "image_url": "https://m.media-amazon.com/images/I/71Em3JXt+kL._AC_SL1500_.jpg",
            "stock": 20,
            "specs": {
                "capacity": "32GB (2x16GB)",
                "speed": "3200MHz",
                "type": "DDR4",
                "cas_latency": "16",
                "voltage": "1.35V",
                "rgb": "No",
                "heat_spreader": "Aluminum",
                "xmp_profiles": "Yes"
            }
        },
        {
            "name": "Crucial Ballistix RGB 16GB",
            "description": "Affordable RGB memory with good overclocking potential.",
            "price": 10999.00,
            "category": "ram",
            "image_url": "https://m.media-amazon.com/images/I/61Rr8uRbPtL._AC_SL1500_.jpg",
            "stock": 22,
            "specs": {
                "capacity": "16GB (2x8GB)",
                "speed": "3600MHz",
                "type": "DDR4",
                "cas_latency": "16",
                "voltage": "1.35V",
                "rgb": "Yes",
                "heat_spreader": "Aluminum",
                "xmp_profiles": "Yes"
            }
        }
    ]
    
    # Storage products
    storages = [
        {
            "name": "Samsung 970 EVO Plus 1TB",
            "description": "High-performance NVMe SSD with excellent endurance and reliability.",
            "price": 14999.00,
            "category": "storage",
            "image_url": "https://m.media-amazon.com/images/I/71A+ZkS3qWL._AC_SL1500_.jpg",
            "stock": 35,
            "specs": {
                "capacity": "1TB",
                "type": "nvme",
                "interface": "PCIe 3.0 x4",
                "seq_read": "3500 MB/s",
                "seq_write": "3300 MB/s",
                "form_factor": "M.2 2280",
                "endurance": "600 TBW",
                "warranty": "5-year limited"
            }
        },
        {
            "name": "Western Digital Black SN850 2TB",
            "description": "Ultra-fast PCIe Gen4 NVMe SSD for gaming and high-performance computing.",
            "price": 29999.00,
            "category": "storage",
            "image_url": "https://m.media-amazon.com/images/I/71DFDbRk0gL._AC_SL1500_.jpg",
            "stock": 18,
            "specs": {
                "capacity": "2TB",
                "type": "nvme",
                "interface": "PCIe 4.0 x4",
                "seq_read": "7000 MB/s",
                "seq_write": "5300 MB/s",
                "form_factor": "M.2 2280",
                "endurance": "1200 TBW",
                "warranty": "5-year limited"
            }
        },
        {
            "name": "Seagate Barracuda 4TB",
            "description": "High-capacity hard drive for storing games, media, and backups.",
            "price": 8999.00,
            "category": "storage",
            "image_url": "https://m.media-amazon.com/images/I/71Czt3SGQzL._AC_SL1500_.jpg",
            "stock": 40,
            "specs": {
                "capacity": "4TB",
                "type": "hdd",
                "interface": "SATA 6 Gb/s",
                "rpm": "5400 RPM",
                "cache": "256MB",
                "form_factor": "3.5-inch",
                "transfer_rate": "190 MB/s",
                "warranty": "2-year limited"
            }
        },
        {
            "name": "Crucial MX500 1TB",
            "description": "Reliable and affordable SATA SSD for system upgrades.",
            "price": 9999.00,
            "category": "storage",
            "image_url": "https://m.media-amazon.com/images/I/81rg-38AdJL._AC_SL1500_.jpg",
            "stock": 28,
            "specs": {
                "capacity": "1TB",
                "type": "sata_ssd",
                "interface": "SATA 6 Gb/s",
                "seq_read": "560 MB/s",
                "seq_write": "510 MB/s",
                "form_factor": "2.5-inch",
                "endurance": "360 TBW",
                "warranty": "5-year limited"
            }
        }
    ]
    
    # PSU products
    psus = [
        {
            "name": "Corsair RM850x",
            "description": "Gold-certified fully modular power supply with silent operation and high efficiency.",
            "price": 16999.00,
            "category": "psu",
            "image_url": "https://m.media-amazon.com/images/I/71BajQzwN4L._AC_SL1500_.jpg",
            "stock": 15,
            "specs": {
                "wattage": "850W",
                "certification": "80+ Gold",
                "modularity": "Fully Modular",
                "fan_size": "135mm",
                "efficiency": "90% at 50% load",
                "protection": "OVP, UVP, OCP, OPP, SCP",
                "connectors": "2x EPS, 4x PCIe, 10x SATA",
                "warranty": "10-year"
            }
        },
        {
            "name": "EVGA SuperNOVA 750 G5",
            "description": "Compact, efficient power supply with excellent build quality and 10-year warranty.",
            "price": 14999.00,
            "category": "psu",
            "image_url": "https://m.media-amazon.com/images/I/71V-Cj7CwNL._AC_SL1500_.jpg",
            "stock": 12,
            "specs": {
                "wattage": "750W",
                "certification": "80+ Gold",
                "modularity": "Fully Modular",
                "fan_size": "135mm",
                "efficiency": "90% at 50% load",
                "protection": "OVP, UVP, OCP, OPP, SCP",
                "connectors": "2x EPS, 4x PCIe, 8x SATA",
                "warranty": "10-year"
            }
        },
        {
            "name": "Seasonic FOCUS GX-650",
            "description": "High-quality, efficient power supply with hybrid fan control for quiet operation.",
            "price": 11999.00,
            "category": "psu",
            "image_url": "https://m.media-amazon.com/images/I/71u-8UqLVTS._AC_SL1500_.jpg",
            "stock": 20,
            "specs": {
                "wattage": "650W",
                "certification": "80+ Gold",
                "modularity": "Fully Modular",
                "fan_size": "120mm",
                "efficiency": "90% at 50% load",
                "protection": "OVP, UVP, OCP, OPP, SCP",
                "connectors": "1x EPS, 2x PCIe, 7x SATA",
                "warranty": "10-year"
            }
        },
        {
            "name": "be quiet! Pure Power 11 600W",
            "description": "Quiet and reliable power supply with good efficiency and cable management.",
            "price": 9999.00,
            "category": "psu",
            "image_url": "https://m.media-amazon.com/images/I/818FEtmLpVL._AC_SL1500_.jpg",
            "stock": 18,
            "specs": {
                "wattage": "600W",
                "certification": "80+ Gold",
                "modularity": "Semi-Modular",
                "fan_size": "120mm",
                "efficiency": "89% at 50% load",
                "protection": "OVP, UVP, OCP, OPP, SCP",
                "connectors": "1x EPS, 2x PCIe, 6x SATA",
                "warranty": "5-year"
            }
        }
    ]
    
    # Case products
    cases = [
        {
            "name": "Corsair 4000D Airflow",
            "description": "Mid-tower ATX case with excellent airflow, easy cable management, and minimalist design.",
            "price": 11999.00,
            "category": "case",
            "image_url": "https://m.media-amazon.com/images/I/71JB3xCeh2L._AC_SL1500_.jpg",
            "stock": 14,
            "specs": {
                "form_factor": "Mid-Tower ATX",
                "dimensions": "453mm x 230mm x 466mm",
                "motherboard_support": "ATX, Micro-ATX, Mini-ITX",
                "expansion_slots": 7,
                "drive_bays": "2x 3.5\", 2x 2.5\"",
                "front_io": "USB 3.0, USB-C, Audio",
                "included_fans": "2x 120mm",
                "radiator_support": "Up to 360mm front, 280mm top"
            }
        },
        {
            "name": "NZXT H510i",
            "description": "Sleek, compact ATX case with integrated RGB and fan controller.",
            "price": 13999.00,
            "category": "case",
            "image_url": "https://m.media-amazon.com/images/I/71p5bK7xylL._AC_SL1500_.jpg",
            "stock": 16,
            "specs": {
                "form_factor": "Mid-Tower ATX",
                "dimensions": "428mm x 210mm x 460mm",
                "motherboard_support": "ATX, Micro-ATX, Mini-ITX",
                "expansion_slots": 7,
                "drive_bays": "2x 3.5\", 3x 2.5\"",
                "front_io": "USB 3.0, USB-C, Audio",
                "included_fans": "2x 120mm",
                "radiator_support": "Up to 280mm front, 120mm rear"
            }
        },
        {
            "name": "Fractal Design Meshify C",
            "description": "Compact ATX case with mesh front panel for maximum airflow and clean aesthetics.",
            "price": 12499.00,
            "category": "case",
            "image_url": "https://m.media-amazon.com/images/I/71khv9D3z5L._AC_SL1500_.jpg",
            "stock": 10,
            "specs": {
                "form_factor": "Mid-Tower ATX",
                "dimensions": "395mm x 212mm x 440mm",
                "motherboard_support": "ATX, Micro-ATX, Mini-ITX",
                "expansion_slots": 7,
                "drive_bays": "2x 3.5\", 3x 2.5\"",
                "front_io": "USB 3.0, Audio",
                "included_fans": "2x 120mm",
                "radiator_support": "Up to 360mm front, 240mm top"
            }
        },
        {
            "name": "Lian Li O11 Dynamic",
            "description": "Premium dual-chamber case with tempered glass panels and excellent water-cooling support.",
            "price": 17999.00,
            "category": "case",
            "image_url": "https://m.media-amazon.com/images/I/718x54yZdIL._AC_SL1500_.jpg",
            "stock": 8,
            "specs": {
                "form_factor": "Mid-Tower ATX",
                "dimensions": "445mm x 272mm x 446mm",
                "motherboard_support": "E-ATX, ATX, Micro-ATX, Mini-ITX",
                "expansion_slots": 8,
                "drive_bays": "6x 2.5\", 3x 3.5\"",
                "front_io": "USB 3.0, USB-C, Audio",
                "included_fans": "None",
                "radiator_support": "360mm side, top, and bottom"
            }
        }
    ]
    
    # Cooling products
    coolings = [
        {
            "name": "Noctua NH-D15",
            "description": "Premium dual-tower CPU air cooler with exceptional cooling performance and quiet operation.",
            "price": 10999.00,
            "category": "cooling",
            "image_url": "https://m.media-amazon.com/images/I/91JefFqUqFL._AC_SL1500_.jpg",
            "stock": 18,
            "specs": {
                "type": "air",
                "socket_support": "Intel & AMD",
                "dimensions": "165mm x 150mm x 161mm",
                "fan_size": "2x 140mm",
                "fan_speed": "300-1500 RPM",
                "noise_level": "24.6 dBA",
                "tdp_rating": "220W",
                "rgb": "No"
            }
        },
        {
            "name": "Corsair iCUE H150i Elite Capellix",
            "description": "High-performance 360mm AIO liquid cooler with RGB pump and fans.",
            "price": 19999.00,
            "category": "cooling",
            "image_url": "https://m.media-amazon.com/images/I/71zRTTRcJJL._AC_SL1500_.jpg",
            "stock": 10,
            "specs": {
                "type": "aio",
                "socket_support": "Intel & AMD",
                "radiator_size": "360mm",
                "fan_size": "3x 120mm",
                "fan_speed": "400-2400 RPM",
                "noise_level": "10-36 dBA",
                "pump_speed": "2400 RPM",
                "rgb": "Yes"
            }
        },
        {
            "name": "be quiet! Dark Rock Pro 4",
            "description": "High-end air cooler with excellent performance and quiet operation.",
            "price": 9999.00,
            "category": "cooling",
            "image_url": "https://m.media-amazon.com/images/I/71Y9Tlg2vpL._AC_SL1500_.jpg",
            "stock": 14,
            "specs": {
                "type": "air",
                "socket_support": "Intel & AMD",
                "dimensions": "146mm x 136mm x 163mm",
                "fan_size": "1x 135mm, 1x 120mm",
                "fan_speed": "1200-1500 RPM",
                "noise_level": "24.3 dBA",
                "tdp_rating": "250W",
                "rgb": "No"
            }
        },
        {
            "name": "NZXT Kraken X63",
            "description": "Elegant 280mm AIO liquid cooler with infinity mirror design and RGB lighting.",
            "price": 16999.00,
            "category": "cooling",
            "image_url": "https://m.media-amazon.com/images/I/71H7fNTmLfL._AC_SL1500_.jpg",
            "stock": 12,
            "specs": {
                "type": "aio",
                "socket_support": "Intel & AMD",
                "radiator_size": "280mm",
                "fan_size": "2x 140mm",
                "fan_speed": "500-1800 RPM",
                "noise_level": "21-38 dBA",
                "pump_speed": "800-2800 RPM",
                "rgb": "Yes"
            }
        }
    ]
    
    # Monitor products
    monitors = [
        {
            "name": "LG 27GL83A-B 27-Inch",
            "description": "27-inch QHD IPS gaming monitor with 144Hz refresh rate and G-Sync compatibility.",
            "price": 34999.00,
            "category": "monitor",
            "image_url": "https://m.media-amazon.com/images/I/81dAe2wXIqL._AC_SL1500_.jpg",
            "stock": 12,
            "specs": {
                "size": "27-inch",
                "resolution": "2560 x 1440 (QHD)",
                "panel_type": "IPS",
                "refresh_rate": "144Hz",
                "response_time": "1ms",
                "adaptive_sync": "G-Sync Compatible",
                "hdr": "HDR10",
                "ports": "2x HDMI, DisplayPort, Headphone Out"
            }
        },
        {
            "name": "Samsung Odyssey G7 32-Inch",
            "description": "32-inch curved QHD gaming monitor with 240Hz refresh rate and 1ms response time.",
            "price": 54999.00,
            "category": "monitor",
            "image_url": "https://m.media-amazon.com/images/I/61Sz8gcsYNL._AC_SL1000_.jpg",
            "stock": 8,
            "specs": {
                "size": "32-inch",
                "resolution": "2560 x 1440 (QHD)",
                "panel_type": "VA Curved (1000R)",
                "refresh_rate": "240Hz",
                "response_time": "1ms",
                "adaptive_sync": "G-Sync & FreeSync Premium Pro",
                "hdr": "HDR600",
                "ports": "2x HDMI, DisplayPort, USB Hub"
            }
        },
        {
            "name": "ASUS TUF Gaming VG259QM 24.5-Inch",
            "description": "24.5-inch FHD gaming monitor with ultra-fast 280Hz refresh rate for competitive gaming.",
            "price": 29999.00,
            "category": "monitor",
            "image_url": "https://m.media-amazon.com/images/I/81cSfIYSUxL._AC_SL1500_.jpg",
            "stock": 15,
            "specs": {
                "size": "24.5-inch",
                "resolution": "1920 x 1080 (FHD)",
                "panel_type": "IPS",
                "refresh_rate": "280Hz",
                "response_time": "1ms",
                "adaptive_sync": "G-Sync Compatible",
                "hdr": "HDR400",
                "ports": "2x HDMI, DisplayPort, Headphone Out"
            }
        },
        {
            "name": "Dell S2721QS 27-Inch",
            "description": "27-inch 4K monitor with excellent color accuracy for productivity and content creation.",
            "price": 32999.00,
            "category": "monitor",
            "image_url": "https://m.media-amazon.com/images/I/71yYGgCG2uL._AC_SL1500_.jpg",
            "stock": 10,
            "specs": {
                "size": "27-inch",
                "resolution": "3840 x 2160 (4K UHD)",
                "panel_type": "IPS",
                "refresh_rate": "60Hz",
                "response_time": "4ms",
                "adaptive_sync": "AMD FreeSync",
                "hdr": "HDR400",
                "ports": "2x HDMI, DisplayPort, Audio Line Out"
            }
        }
    ]
    
    # Prebuilt PC products
    prebuilt_pcs = [
        {
            "name": "Intel Gaming Beast",
            "description": "High-end gaming PC with Intel Core i9 CPU and RTX 3080 GPU for ultimate gaming performance.",
            "price": 249999.00,
            "category": "prebuilt",
            "image_url": "https://m.media-amazon.com/images/I/71Lczneb4dL._AC_SL1500_.jpg",
            "stock": 5,
            "specs": {
                "cpu": "Intel Core i9-12900K",
                "gpu": "NVIDIA GeForce RTX 3080 10GB",
                "ram": "32GB DDR4 3600MHz",
                "storage": "2TB NVMe SSD + 2TB HDD",
                "motherboard": "Z690 ATX",
                "psu": "850W 80+ Gold",
                "cooling": "360mm AIO Liquid Cooler",
                "case": "Premium ATX Mid-Tower"
            }
        },
        {
            "name": "AMD Productivity Powerhouse",
            "description": "High-performance PC with AMD Ryzen 9 processor for content creation, streaming, and gaming.",
            "price": 219999.00,
            "category": "prebuilt",
            "image_url": "https://m.media-amazon.com/images/I/81qVTu1u6wL._AC_SL1500_.jpg",
            "stock": 4,
            "specs": {
                "cpu": "AMD Ryzen 9 5950X",
                "gpu": "AMD Radeon RX 6800 XT 16GB",
                "ram": "64GB DDR4 3200MHz",
                "storage": "1TB NVMe SSD + 4TB HDD",
                "motherboard": "X570 ATX",
                "psu": "750W 80+ Gold",
                "cooling": "280mm AIO Liquid Cooler",
                "case": "Premium ATX Mid-Tower"
            }
        },
        {
            "name": "Intel Mid-Range Gaming PC",
            "description": "Great value gaming PC with Intel Core i5 and RTX 3060 Ti for high-fps 1080p and 1440p gaming.",
            "price": 149999.00,
            "category": "prebuilt",
            "image_url": "https://m.media-amazon.com/images/I/71XorDHIN+L._AC_SL1500_.jpg",
            "stock": 8,
            "specs": {
                "cpu": "Intel Core i5-12600K",
                "gpu": "NVIDIA GeForce RTX 3060 Ti 8GB",
                "ram": "16GB DDR4 3200MHz",
                "storage": "1TB NVMe SSD",
                "motherboard": "B660 ATX",
                "psu": "650W 80+ Bronze",
                "cooling": "Air Cooler",
                "case": "ATX Mid-Tower"
            }
        },
        {
            "name": "AMD Budget Gaming PC",
            "description": "Affordable gaming PC with AMD Ryzen 5 and RX 6600 XT for excellent 1080p gaming performance.",
            "price": 119999.00,
            "category": "prebuilt",
            "image_url": "https://m.media-amazon.com/images/I/71DTUKpTYaL._AC_SL1500_.jpg",
            "stock": 10,
            "specs": {
                "cpu": "AMD Ryzen 5 5600X",
                "gpu": "AMD Radeon RX 6600 XT 8GB",
                "ram": "16GB DDR4 3200MHz",
                "storage": "500GB NVMe SSD + 1TB HDD",
                "motherboard": "B550 ATX",
                "psu": "550W 80+ Bronze",
                "cooling": "Air Cooler",
                "case": "ATX Mid-Tower"
            }
        }
    ]
    
    # Combine all products
    all_products = cpus + motherboards + gpus + rams + storages + psus + cases + coolings + monitors + prebuilt_pcs
    
    # Create all products
    for product_data in all_products:
        # Extract specs
        specs = product_data.pop("specs", {})
        
        # Create product instance
        product = Product(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            category=product_data["category"],
            image_url=product_data["image_url"],
            stock=product_data["stock"],
            specs=specs
        )
        db.session.add(product)
    
    # Commit all products
    db.session.commit()
    print(f"Created {len(all_products)} products.")
    
    # Return count of created products
    return len(all_products)


if __name__ == "__main__":
    from app import app
    
    with app.app_context():
        db.create_all()
        create_admin_user()
        create_test_user()
        product_count = create_products()
        print(f"Database seeding complete. Created {product_count} products.")