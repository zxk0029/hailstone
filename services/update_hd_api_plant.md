# Update Plan for api/wallet/hd_api_v1.py

This plan details the steps required to refactor `api/wallet/hd_api_v1.py` to use the new separated gRPC clients (`AccountClient` and `UtxoClient`) based on the chain's model type.

## Tasks

1.  **Update Imports:**
    *   Remove `from services.wallet_client import WalletClient`.
    *   Add `from services.account_client import AccountClient`.
    *   Add `from services.utxo_client import UtxoClient`.
    *   Add `from common.models import Chain` (if not already imported).
    *   Add `from common.helpers import error_json` (if not already imported).
    *   Add `from services.savour_rpc import common_pb2` (needed for result code checks).
    *   Add `from decimal import Decimal` (if needed for balance conversion).
    *   Add `from api.wallet.types import AddressTransaction` (if needed).


2.  **Define Helper Function:**
    *   Define a new helper function `get_rpc_client_by_chain(chain_name: str)` within the file.
    *   This function will:
        *   Take `chain_name` as input.
        *   Query the `Chain` model for the given name.
        *   If the chain is not found, return `(None, "Chain not found")`.
        *   Check the `model_type` field of the `Chain` object.
        *   If `model_type` is 'ACCOUNT', return `(AccountClient(), None)`.
        *   If `model_type` is 'UTXO', return `(UtxoClient(), None)`.
        *   Otherwise, return `(None, "Unsupported model_type ...")`.

3.  **Refactor API Functions:**
    *   Modify **all** functions that previously used `WalletClient` (e.g., `get_balance`, `get_nonce`, `get_account_info`, `get_fee`, `get_sign_tx_info`, `send_transaction`, `get_address_transaction`, `get_hash_transaction`, `get_unspend_list`).
    *   For each function:
        *   Call the `get_rpc_client_by_chain(chain)` helper function at the beginning to get the `client` instance and potential `error_msg`.
        *   Check if `client` is `None`. If so, return `error_json(error_msg, 4000)`.
        *   Replace the old `wallet_client.method_call(...)` with `client.corresponding_method_call(...)`.
        *   **Crucially adapt the logic:**
            *   **Parameter Mapping:** Ensure the parameters passed to the new client methods match the definitions in `AccountClient` or `UtxoClient`.
            *   **Response Handling:** Adapt the code to handle the response structures returned by the new client methods (which correspond to `account.proto` or `utxo.proto`). Check the `result.code == common_pb2.SUCCESS` pattern.
            *   **Model-Specific Logic:** Use `isinstance(client, AccountClient)` or `isinstance(client, UtxoClient)` to conditionally execute logic or call methods specific to one model type.
                *   Example: `get_nonce` should only attempt to get `result.sequence` if `isinstance(client, AccountClient)`.
                *   Example: `get_unspend_list` should likely only work if `isinstance(client, UtxoClient)`.
            *   **Shared Method Handling:** For methods present in both clients (like `get_account`, `get_fee`, `send_tx`), ensure the code correctly handles the potentially different request/response fields for ACCOUNT vs. UTXO chains.
            *   **Balance/Unit Conversion:** Review how balances are handled (e.g., division by `db_asset.unit`). Ensure this logic is still correct with the new response structures.
            *   **Error Handling:** Maintain or improve existing error handling (e.g., `try...except` blocks).

4.  **Testing:**
    *   Thoroughly test all modified API endpoints.
    *   Ensure tests cover both ACCOUNT-based chains (e.g., Ethereum) and UTXO-based chains (e.g., Bitcoin).
    *   Verify correct data retrieval, transaction submission, and error handling for both model types.
