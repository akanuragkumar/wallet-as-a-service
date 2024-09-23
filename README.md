# Wallet-as-a-Service
======================

## [API Documentation](https://akanuragkumar.github.io/wallet-as-a-service/)

## Overview
------------

Wallet-as-a-Service is a Django-based project that provides a scalable and secure wallet management system for businesses and individuals. The project aims to provide a robust and reliable platform for managing digital wallets, transactions, and customer data.

## Features
------------

*   **Multi-tenancy**: Support for multiple tenants, allowing businesses to manage their own wallets and customers.
*   **Shared Database & Shared Tables**: All tenants share the same tables, simplifying database management.
*   **Tenant-Aware Queries**: Middleware dynamically identifies the tenant and filters queries by `tenant_id` to ensure data isolation.
*   **Single Database, Single Schema**: No need for separate schemas for each tenant.
*   **Scalability**: This architecture scales well for tenants that don't require significant isolation.
*   **Simplified Migrations**: Apply migrations once, and they will be applied to all tenants sharing the same tables.
*   **Customer Management**: Manage customer information, including profiles, wallets, and transaction history.
*   **Wallet Management**: Create, manage, and update digital wallets, including balance management and transaction processing.
*   **Transaction Management**: Process transactions, including payments, transfers, and withdrawals.
*   **Security**: Implement robust security measures, including encryption, authentication, and authorization.

**How it Works**
----------------

1. Each table in the database has a `tenant_id` column.
2. When a tenant makes a request, the middleware identifies the tenant and appends a filter to the query to only retrieve data for that tenant.
3. The database returns only the data for the requesting tenant, ensuring data isolation.

**Benefits**
------------

* Simplified database management
* Scalable architecture
* Easy migration management

## Technical Requirements
-------------------------

*   **Python**: 3.8+
*   **Django**: 5.1.1
*   **Database**: PostgreSQL
*   **Dependencies**: See `requirements.txt` for a list of dependencies.

## Installation
------------

1.  Clone the repository: `git clone https://github.com/your-username/wallet-as-a-service.git`
2.  Install dependencies: `pip install -r requirements.txt`
3.  Create a new PostgreSQL database: `createdb wallet_as_a_service`
4.  Configure environment variables: `cp .env.example .env` and update the variables as needed.
5.  Run migrations: `python manage.py migrate`
6.  Start the development server: `python manage.py runserver`

## API Documentation
-------------------

API documentation is available at `/api/docs/`.
