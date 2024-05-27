class UnissuedInvoicesError(Exception):
    """
    Error indicates that no invoices were issued for this account

    Args:
        Exception (Exception): No invoices were issued.
    """
    pass


class DownloadInvoiceError(Exception):
    """
    Error indicates that there was an error downloading the invoice

    Args:
        Exception (Exception): Error downloading invoice
    """
    pass
