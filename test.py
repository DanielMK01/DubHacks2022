from sapling import SaplingClient

def main():
    API_KEY = 'GVN4N2YHFS5TQRJPKYQJSPVSXZQSK70H'
    client = SaplingClient(api_key=API_KEY)
    edits = client.edits('Lets get started!', session_id='test_session')
    print(edits)