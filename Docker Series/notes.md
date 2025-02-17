# Why Containers?

Suppose mai ek Windows machine pr kaam kar raha hoon aur maine ek DS-application bana di. Is application mein maine bohot saari dependencies install kari hain.

Agar koi aur developer mera project use karna chahe, toh unhe bhi wahi dependencies install karni padegi. Lekin, is baat ka chance hai ki kuch functionality sahi se kaam na kare. (version mismatch or any other differences)

## Containers
- Ek tarika hai jisme hum apni application ko saari zaruri dependencies aur configurations ke sath package karte hain.
- Portable artifact hota hai, jise easily kisi bhi environment mein share ya move kiya ja sakta hai.
- Isse development aur deployment zyada asaan, efficient aur synced ho jata hai.

---

# Docker Image aur Containers

### Containers
- Docker images ka ek collection hota hai.
- Har dependency ki ek image ban sakti hai.
- Saari dependencies ke complete layers ka ek set banta hai jise docker image kehte hain.

### Docker Image
- Ek package/artifact hota hai, jise move ya share kiya ja sakta hai.
- Jab docker image ko run karte hain, toh ek application environment create hota hai aur wahi environment mein application run hoti hai.

### Container
- Application ko start karne ke liye container create hota hai.
- Container ek environment create karta hai jisme application chalti hai.


# Docker vs Virtual Machines (both ka purpose virualisation )

operating system
