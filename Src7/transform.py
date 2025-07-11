import re
from connection import sqlserver
def transform(text):
    name=text.split('\n')[0]
    print(name)
    phone_match = re.search(r'(\(?\+91\)?[\s-]?|0)?[6789]\d{9}', text)
    Phone = phone_match.group() if phone_match else None

    print(Phone)
    email_match=re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    Email = email_match.group() if email_match else None
    print(Email)
    skills_list = [
        # 🖥️ Programming Languages
        'python', 'java', 'c', 'c++', 'c#', 'javascript', 'typescript',
        'ruby', 'php', 'swift', 'go', 'rust', 'kotlin',
        'bash', 'shell scripting', 'matlab', 'objective-c', 'perl',
 
        # 🧱 Frameworks & Libraries
        'django', 'flask', 'fastapi', 'spring boot', 'express.js',
        'react', 'angular', 'vue.js', 'next.js', 'nestjs',
        'jquery', 'bootstrap', 'tailwind css', 'dotnet', 'laravel',
        'tensorflow', 'keras', 'pytorch', 'scikit-learn', 'opencv',
 
        # 🗄️ Databases
        'mysql', 'postgresql', 'sqlite', 'mongodb', 'oracle',
        'sql server', 'redis', 'cassandra', 'couchbase',
        'elasticsearch', 'dynamodb', 'firebase realtime db','sql',
 
        # ☁️ Cloud Platforms
        'aws', 'azure', 'google cloud platform', 'gcp',
        'heroku', 'digitalocean', 'netlify', 'vercel',
 
        # 🛠️ DevOps & Tools
        'docker', 'kubernetes', 'jenkins', 'terraform', 'ansible',
        'git', 'github', 'gitlab', 'bitbucket', 'circleci',
        'travis ci', 'vagrant', 'helm',
 
        # 📊 Data & Analytics
        'pandas', 'numpy', 'matplotlib', 'seaborn', 'power bi',
        'tableau', 'excel', 'hadoop', 'spark', 'airflow',
        'apache kafka', 'databricks', 'bigquery',
 
        # 🔒 Security & Networking
        'linux', 'windows server', 'firewall', 'ssl', 'tcp/ip',
        'ethical hacking', 'penetration testing', 'nmap',
        'wireshark', 'burpsuite', 'cybersecurity', 'oauth',
 
        # 🌐 Web & API Tech
        'html', 'css', 'sass', 'graphql', 'rest api', 'soap',
        'postman', 'swagger', 'json', 'xml',
 
   
 
        # 🎨 Design Tools
        'figma', 'adobe xd', 'photoshop', 'illustrator',
        'canva', 'blender', 'invision'
        ]
    low_text=text.lower()
    skills=[]
    for skill in skills_list:
        pattern=r'\b'+re.escape(skill)+r'\b'
        if re.search(pattern,low_text):
            skills.append(skill)

    skills=','.join(skills)
    print(skills)

    connection=sqlserver()
    cusor=connection.cursor()
    cusor.execute("insert into resume(Name,phone,Email,Technical_skills) values(?,?,?,?)",name,Phone,Email,skills)
    connection.commit()
    connection.close()



 
                    