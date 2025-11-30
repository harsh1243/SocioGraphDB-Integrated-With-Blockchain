🐦 Mini Twitter (Web3 Integrated)

A decentralized "SocialFi" platform that bridges the gap between traditional social media and the Sui Blockchain.

📖 Overview

Mini Twitter is a Proof-of-Concept (PoC) application demonstrating a custodial SocialFi architecture. Unlike typical Web3 dApps that require browser extensions, this platform acts as a custodian that generates and stores user private keys directly within the application's secure database, removing the complexity of self-custody for the end user.

Unlike traditional platforms, every user on Mini Twitter is automatically provisioned a Sui Blockchain Wallet upon registration. This invisible wallet creation allows users to engage in SocialFi activities—such as tipping content creators or managing crypto assets—without needing external browser extensions or complex setup.

✨ Key Features

📱 Social Experience

Identity Management: Secure signup and login system using password hashing (SHA-256).

Multimedia Feed: Users can post text updates and upload images, which are stored securely on the server.

Rich Interactions: The platform supports liking, replying, and bookmarking posts.

Social Graph: A complete follow/unfollow system with a dedicated "Explore" tab to discover new users.

Direct Messaging: Private, real-time communication between users.

Notifications: Real-time alerts for social interactions.

🔗 Web3 & SocialFi Integration

Embedded Wallet System:

Automatically generates a 12-word mnemonic phrase and Ed25519 keypair for every new user.

Wallets are native to the application, lowering the barrier to entry for non-crypto users.

Asset Dashboard: A built-in wallet interface showing real-time SUI balance and current USD valuation (via CoinGecko API).

Micro-Tipping: Users can send SUI tokens directly to others from their profile pages, monetizing social interactions.

Funds Management: Full capability to withdraw funds to external wallets.

🛠️ Technical Architecture

The project is built using a modular Python architecture, separating the User Interface, Database Logic, and Blockchain interactions into distinct layers.

Technology Stack

Component

Technology

Description

Frontend

Streamlit

Provides the reactive web interface and component rendering.

Backend Logic

Python 3

Handles business logic, authentication, and routing.

Database

SQLite

Lightweight, file-based relational database for storing user data, posts, and relationships.

Blockchain

PySUI

Python client SDK for interacting with the Sui Fullnode RPC.

Styling

Custom CSS

Overrides default Streamlit styles for a "Dark Mode" Twitter-like aesthetic.

Code Structure

The codebase is organized to support scalability and ease of understanding:

/my-web3-twitter
│
├── main.py                # Application Entry Point: Handles UI routing and session state
├── config.py              # Configuration: Global constants, paths, and RPC URLs
├── database.py            # Data Layer: SQL connection management and schema initialization
├── crud.py                # Logic Layer: All database operations (Create, Read, Update, Delete)
├── blockchain.py          # Web3 Layer: PySUI logic for wallet generation and transactions
├── components.py          # UI Components: Reusable widgets (Post cards, User lists, Chat)
├── utils.py               # Utilities: Helper functions for hashing, time formatting, and images
└── twitter_clone.db       # Persistence: Local SQL database file


