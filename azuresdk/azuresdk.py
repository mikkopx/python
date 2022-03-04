import os

from azure.identity import AzureCliCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.storage.blob import BlobClient
from azure.storage.blob import BlobServiceClient
from azure.keyvault.secrets import SecretClient

credential = AzureCliCredential()
subscription_id = os.environ["SUBSCRIPTION_ID"]
resource_client = ResourceManagementClient(credential, subscription_id)
storage_client = StorageManagementClient(credential, subscription_id)
network_client = NetworkManagementClient(credential, subscription_id)
compute_client = ComputeManagementClient(credential, subscription_id)
client = SecretClient(vault_url="https://mikko-vault.vault.azure.net/", credential = credential)

#DEFINITIONS FOR RESOURCES
GROUP_NAME = "resourcegrouop"
STORAGE_ACCOUNT = "storage"
BLOB_CONTAINER = "blobcontainer"
VIRTUAL_NETWORK_NAME = "vnet01"
SUBNET_NAME = "sn01"
PREFIX = "10.0.0.0/24"
VM_NAME = "ls01"
MY_CONN = "" #ACCESS KEY FROM STORAGE ACCOUNT

def rg_list():

    group_list = resource_client.resource_groups.list()
    column_width = 40
    print("Resource Group".ljust(column_width) + "Location")
    print("-" * (column_width * 2))
    for group in list(group_list):
        print(f"{group.name:<{column_width}}{group.location}")

def rg_create(GROUP_NAME):

    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "westeurope"})
    print(f"Resource Group {GROUP_NAME} was created")

def rg_get(GROUP_NAME):

    resource_list = resource_client.resources.list_by_resource_group(GROUP_NAME, expand = "createdTime,changedTime")
    column_width = 36

    print("Resource".ljust(column_width) + "Type".ljust(column_width)
    + "Create date".ljust(column_width) + "Change date".ljust(column_width))
    print("-" * (column_width * 4))

    for resource in list(resource_list):
        print(f"{resource.name:<{column_width}}{resource.type:<{column_width}}"
        f"{str(resource.created_time):<{column_width}}{str(resource.changed_time):<{column_width}}")

def rg_delete(GROUP_NAME):

    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()
    print(f"Resource Group {GROUP_NAME} was deleted")

def storageaccount_create(GROUP_NAME, STORAGE_ACCOUNT):

    storage_client.storage_accounts.begin_create(
        GROUP_NAME,
        STORAGE_ACCOUNT,
        {
            "sku": {
                "name": "Standard_GRS"
            },
            "kind": "StorageV2",
            "location": "WestEurope",
            "encryption": {
                "services": {
                    "file": {
                        "key_type": "Account",
                        "enabled": True
                    },
                    "blob": {
                        "key_type": "Account",
                        "enabled": True
                    }
                },
                "key_source": "Microsoft.Storage"
            },
            "tags": {
                "key1": "value1",
                "key2": "value2"
            }
        }
    ).result()
    
    print(f"Storage Account {STORAGE_ACCOUNT} created to {GROUP_NAME}")

def storageaccount_delete(GROUP_NAME, STORAGE_ACCOUNT):

    storage_client.storage_accounts.delete(
        GROUP_NAME,
        STORAGE_ACCOUNT,
    )
    
    print(f"Storage Account {STORAGE_ACCOUNT} was deleted")


def blobcontainer_create(GROUP_NAME, STORAGE_ACCOUNT, BLOB_CONTAINER):
    
    blob_container = storage_client.blob_containers.create(
        GROUP_NAME,
        STORAGE_ACCOUNT,
        BLOB_CONTAINER,
        {}
    )
    print(f"Blob Container {BLOB_CONTAINER} added to {STORAGE_ACCOUNT}")

def blobcontainer_delete(GROUP_NAME, STORAGE_ACCOUNT, BLOB_CONTAINER):

    blob_container = storage_client.blob_containers.delete(
        GROUP_NAME,
        STORAGE_ACCOUNT,
        BLOB_CONTAINER
    )
    print(f"Blob container {BLOB_CONTAINER} was deleted")

def vnet_list(GROUP_NAME):

    result_create = network_client.virtual_networks.list(
        GROUP_NAME,
    )
    for re in result_create:
        print(re.name)

def vnet_create(GROUP_NAME, VIRTUAL_NETWORK_NAME):

    network = network_client.virtual_networks.begin_create_or_update(
        GROUP_NAME,
        VIRTUAL_NETWORK_NAME,
        {
            "address_space": {
                "address_prefixes": [
                    "10.0.0.0/16"
                ]
            },
            "location": "westeurope"
        }
    ).result()
    print(f"Virtual Network {VIRTUAL_NETWORK_NAME} was created")

def vnet_delete(GROUP_NAME, VIRTUAL_NETWORK_NAME):
    network = network_client.virtual_networks.begin_delete(
        GROUP_NAME,
        VIRTUAL_NETWORK_NAME)
    print(f"Virtual Network {VIRTUAL_NETWORK_NAME} was deleted")

def subnet_create(GROUP_NAME, VIRTUAL_NETWORK_NAME, SUBNET_NAME, CIDR):

    subnet = network_client.subnets.begin_create_or_update(
        GROUP_NAME,
        VIRTUAL_NETWORK_NAME,
        SUBNET_NAME,
        {
            "address_prefix": CIDR
        }
    ).result()
    print(f"Subnet {SUBNET_NAME} with prefix {CIDR} was created to {VIRTUAL_NETWORK_NAME}")

def subnet_delete(GROUP_NAME, VIRTUAL_NETWORK_NAME, SUBNET_NAME):

    subnet = network_client.subnets.begin_delete(
        GROUP_NAME,
        VIRTUAL_NETWORK_NAME,
        SUBNET_NAME
    ).result()
    print(f"Subnet {SUBNET_NAME} was deleted")

def vm_list(GROUP_NAME):
    result_create = compute_client.virtual_machines.list(
        GROUP_NAME,
    )
    for re in result_create:
        print(re.name)

def vm_stop(GROUP_NAME, VM_NAME):
    print(f"Virtual Machine {VM_NAME} stopped")
    async_vm_stop = compute_client.virtual_machines.begin_power_off(
        GROUP_NAME, VM_NAME)
    async_vm_stop.wait()

def vm_start(GROUP_NAME, VM_NAME):
    print(f"Virtual Machine {VM_NAME} started")
    async_vm_stop = compute_client.virtual_machines.begin_start(
        GROUP_NAME, VM_NAME)
    async_vm_stop.wait()

def blob_upload(file, blobi):

    blob = BlobClient.from_connection_string(conn_str=(MY_CONN)
    , container_name=(BLOB_CONTAINER), blob_name=(blobi))
    with open(file, "rb") as data:
        blob.upload_blob(data)
        print(f"file was uploaded to {BLOB_CONTAINER}!")

def blob_download(blobi):

    blob = BlobClient.from_connection_string(conn_str=(MY_CONN)
    , container_name=(BLOB_CONTAINER), blob_name=(blobi))
    with open(blobi, "wb") as my_blob:
        blob_data = blob.download_blob()
        blob_data.readinto(my_blob)
        print(f"file was downloaded from {BLOB_CONTAINER}!")

def blob_delete(blobi):

    blob = BlobClient.from_connection_string(conn_str=(MY_CONN)
    , container_name=(BLOB_CONTAINER), blob_name=(blobi))
    blob.delete_blob(delete_snapshots=False)
    print(f"file was deleted from {BLOB_CONTAINER}!")

def secret_get(secret_name):

    secret = client.get_secret(secret_name)
    print(f"Secret value is {secret.value}")

def secret_create(secret_name, secret_value):

    client.set_secret(secret_name, secret_value)
    retrieved_secret = client.get_secret(secret_name)
    print(retrieved_secret)

def blob_upload_with_secret(file, blobi, secret_name):

    secret = client.get_secret(secret_name)
    MY_CONN = secret.value
    blob = BlobClient.from_connection_string(conn_str=(MY_CONN)
    , container_name=(BLOB_CONTAINER), blob_name=(blobi))
    with open(file, "rb") as data:
        blob.upload_blob(data)
        print(f"file was uploaded to {BLOB_CONTAINER}!")


#DRIVECOMMANDS

#rg_create(GROUP_NAME)
#rg_get(GROUPNAME)
#rg_list()
#rg_delete(GROUP_NAME)
#storageaccount_create(GROUP_NAME, STORAGE_ACCOUNT)
#storageaccount_delete(GROUP_NAME, STORAGE_ACCOUNT)
#blobcontainer_create(GROUP_NAME, STORAGE_ACCOUNT, BLOB_CONTAINER)
#blobcontainer_delete(GROUP_NAME, STORAGE_ACCOUNT, BLOB_CONTAINER)
#vnet_list(GROUP_NAME)
#vnet_create(GROUP_NAME, VIRTUAL_NETWORK_NAME)
#vnet_delete(GROUP_NAME, VIRTUAL_NETWORK_NAME)
#subnet_create(GROUP_NAME, VIRTUAL_NETWORK_NAME, SUBNET_NAME, PREFIX)
#subnet_delete(GROUP_NAME, VIRTUAL_NETWORK_NAME, SUBNET_NAME)
#vm_list(GROUP_NAME)
#vm_stop(GROUP_NAME, VM_NAME)
#vm_start(GROUP_NAME, VM_NAME)
#blob_upload("upload.txt", "upload2.txt")
#blob_download("upload2.txt")
#blob_delete("upload2.txt")
#secret_get("salaisuus01")
#secret_create("salaisuus01", "TosiSalainen1!")
#blob_upload_with_secret('upload.txt', 'upload2.txt', 'salaisuus01')