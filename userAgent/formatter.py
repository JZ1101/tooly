"""
Response Formatter - Formats tool responses for user-friendly display
"""

import json
import re
from typing import Dict, Any, Union
from decimal import Decimal

class ResponseFormatter:
    """Formats tool responses for end users"""
    
    def __init__(self):
        # Common token symbols and their display names
        self.token_names = {
            'ETH': 'Ethereum',
            'BTC': 'Bitcoin', 
            'USDC': 'USD Coin',
            'USDT': 'Tether',
            'DAI': 'DAI Stablecoin',
            'WETH': 'Wrapped Ethereum'
        }
    
    def format_balance(self, raw_response: Union[str, Dict[str, Any]]) -> str:
        """
        Format balance response for user display
        
        Args:
            raw_response: Raw response from balance tool
            
        Returns:
            User-friendly balance message
        """
        try:
            # Handle string responses (from placeholder functions)
            if isinstance(raw_response, str):
                return self._format_string_response(raw_response, "balance")
            
            # Handle structured responses (from actual spoonOS)
            if isinstance(raw_response, dict):
                balance = raw_response.get('balance', '0')
                token = raw_response.get('token', 'tokens')
                decimals = raw_response.get('decimals', 18)
                
                # Convert balance from wei/smallest unit
                readable_balance = self._format_token_amount(balance, decimals)
                token_display = self.token_names.get(token, token)
                
                return f"💰 You have **{readable_balance} {token}** ({token_display}) in your wallet"
                
        except Exception as e:
            return f"❌ Unable to format balance information. Raw data: {raw_response}"
    
    def format_transaction_history(self, raw_response: Union[str, Dict[str, Any]]) -> str:
        """Format transaction history for user display"""
        try:
            if isinstance(raw_response, str):
                return self._format_string_response(raw_response, "transactions")
            
            if isinstance(raw_response, dict):
                transactions = raw_response.get('transactions', [])
                
                if not transactions:
                    return "📋 No transactions found for this address"
                
                formatted = "📋 **Recent Transactions:**\n\n"
                
                for i, tx in enumerate(transactions[:5], 1):  # Show max 5
                    tx_hash = self._truncate_hash(tx.get('hash', 'Unknown'))
                    amount = self._format_token_amount(
                        tx.get('value', '0'), 
                        tx.get('decimals', 18)
                    )
                    token = tx.get('token', 'ETH')
                    tx_type = tx.get('type', 'transfer').capitalize()
                    
                    formatted += f"{i}. **{tx_type}** - {amount} {token}\n"
                    formatted += f"   Hash: `{tx_hash}`\n\n"
                
                return formatted
                
        except Exception as e:
            return f"❌ Unable to format transaction history. Raw data: {raw_response}"
    
    def format_gas_estimate(self, raw_response: Union[str, Dict[str, Any]]) -> str:
        """Format gas estimate for user display"""
        try:
            if isinstance(raw_response, str):
                return self._format_string_response(raw_response, "gas")
            
            if isinstance(raw_response, dict):
                gas_limit = raw_response.get('gas_limit', 0)
                gas_price = raw_response.get('gas_price', 0)
                total_cost_usd = raw_response.get('total_cost_usd', 0)
                network = raw_response.get('network', 'Ethereum')
                
                formatted = f"⛽ **Gas Estimate ({network}):**\n\n"
                formatted += f"• Gas Limit: {gas_limit:,} units\n"
                formatted += f"• Gas Price: {gas_price:.2f} gwei\n"
                formatted += f"• **Estimated Cost: ${total_cost_usd:.2f} USD**\n\n"
                formatted += "💡 *Gas prices fluctuate. Execute soon for accurate costs.*"
                
                return formatted
                
        except Exception as e:
            return f"❌ Unable to format gas estimate. Raw data: {raw_response}"
    
    def format_contract_execution(self, raw_response: Union[str, Dict[str, Any]]) -> str:
        """Format contract execution result for user display"""
        try:
            if isinstance(raw_response, str):
                return self._format_string_response(raw_response, "contract")
            
            if isinstance(raw_response, dict):
                success = raw_response.get('success', False)
                tx_hash = raw_response.get('transaction_hash', '')
                gas_used = raw_response.get('gas_used', 0)
                
                if success:
                    formatted = "✅ **Contract Execution Successful!**\n\n"
                    formatted += f"• Transaction Hash: `{self._truncate_hash(tx_hash)}`\n"
                    formatted += f"• Gas Used: {gas_used:,} units\n\n"
                    formatted += "🔗 View on explorer for full details"
                else:
                    error = raw_response.get('error', 'Unknown error')
                    formatted = "❌ **Contract Execution Failed**\n\n"
                    formatted += f"• Error: {error}\n"
                    formatted += "💡 Check parameters and try again"
                
                return formatted
                
        except Exception as e:
            return f"❌ Unable to format contract execution result. Raw data: {raw_response}"
    
    def format_error(self, error: Exception, context: str = "") -> str:
        """Convert technical errors to user-friendly messages"""
        error_msg = str(error).lower()
        
        # Map common errors to user-friendly messages
        if 'network' in error_msg or 'connection' in error_msg:
            return "🌐 Network connection issue. Please check your internet and try again."
        elif 'insufficient' in error_msg and 'balance' in error_msg:
            return "💰 Insufficient balance to complete this transaction."
        elif 'gas' in error_msg:
            return "⛽ Gas-related error. The transaction may cost more than expected."
        elif 'invalid' in error_msg and 'address' in error_msg:
            return "📍 Invalid wallet address format. Please check and try again."
        elif 'timeout' in error_msg:
            return "⏱️ Request timed out. The network might be congested. Please try again."
        else:
            base_msg = f"❌ I encountered an issue"
            if context:
                base_msg += f" while {context}"
            base_msg += ". Please try rephrasing your request or contact support."
            return base_msg
    
    def _format_string_response(self, response: str, response_type: str) -> str:
        """Format string responses from placeholder functions"""
        # Add appropriate emoji based on response type
        emoji_map = {
            'balance': '💰',
            'transactions': '📋', 
            'gas': '⛽',
            'contract': '📝'
        }
        
        emoji = emoji_map.get(response_type, '🔍')
        return f"{emoji} {response}"
    
    def _format_token_amount(self, amount: Union[str, int], decimals: int = 18) -> str:
        """Format token amount with proper decimal places"""
        try:
            # Convert from smallest unit (wei) to readable amount
            amount_decimal = Decimal(str(amount)) / (10 ** decimals)
            
            # Format with appropriate decimal places
            if amount_decimal >= 1000:
                return f"{amount_decimal:,.2f}"
            elif amount_decimal >= 1:
                return f"{amount_decimal:.4f}"
            else:
                return f"{amount_decimal:.6f}".rstrip('0').rstrip('.')
                
        except (ValueError, TypeError):
            return str(amount)
    
    def _truncate_hash(self, hash_str: str, length: int = 10) -> str:
        """Truncate transaction hash for display"""
        if len(hash_str) <= length:
            return hash_str
        return f"{hash_str[:length//2]}...{hash_str[-length//2:]}"

# Example usage for testing
if __name__ == "__main__":
    formatter = ResponseFormatter()
    
    # Test balance formatting
    balance_response = {
        'balance': '1000000000000000000',  # 1 ETH in wei
        'token': 'ETH',
        'decimals': 18
    }
    print("Balance:", formatter.format_balance(balance_response))
    
    # Test transaction formatting  
    tx_response = {
        'transactions': [
            {
                'hash': '0x123456789abcdef123456789abcdef123456789abcdef',
                'value': '500000000000000000',
                'token': 'ETH',
                'decimals': 18,
                'type': 'transfer'
            }
        ]
    }
    print("\nTransactions:", formatter.format_transaction_history(tx_response))