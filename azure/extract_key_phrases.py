"""
https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/textanalytics/azure-ai-textanalytics/samples/sample_extract_key_phrases.py

Parking this for now - the results haven't been particularly useful. e.g. not identifying the phrase 'data center'

DESCRIPTION:
    This sample demonstrates how to extract key talking points from a batch of documents.

    In this sample, we want to go over articles and read the ones that mention Microsoft.
    We're going to use the SDK to create a rudimentary search algorithm to find these articles.

USAGE:
    python sample_extract_key_phrases.py

    Set the environment variables with your own values before running the sample:
    1) AZURE_LANGUAGE_ENDPOINT - the endpoint to your Language resource.
    2) AZURE_LANGUAGE_KEY - your Language subscription key
"""


def sample_extract_key_phrases() -> None:
    # [START extract_key_phrases]
    import os
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.textanalytics import TextAnalyticsClient

    endpoint = os.environ["AZURE_LANGUAGE_ENDPOINT"]
    key = os.environ["AZURE_LANGUAGE_KEY"]

    text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    articles = [
        """
        Genetic-Based Virtual Machines Consolidation Strategy With Efficient Energy Consumption in Cloud Environment
        """,
        """
        Implementing green technologies and practices in a high performance computing center
        """,
        """
        Optimizing Cloud Data Center Energy Efficiency via Dynamic Prediction of {CPU} Idle Intervals
        """,
        """
        Software sustainability requirements: a unified method for improving requirements process for software development
        """
    ]

    result = text_analytics_client.extract_key_phrases(articles)
    for idx, doc in enumerate(result):
        if not doc.is_error:
            print("Key phrases in article #{}: {}".format(
                idx + 1,
                ", ".join(doc.key_phrases)
            ))


if __name__ == '__main__':
    sample_extract_key_phrases()