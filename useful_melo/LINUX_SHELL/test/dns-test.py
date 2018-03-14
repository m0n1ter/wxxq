import dns.resolver
domain = 'www.0551live.com'
answers = dns.resolver.query(domain, 'A')
for answer in answers:
    print answer.to_text()
