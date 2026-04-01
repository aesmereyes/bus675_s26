# Lab 2 Reflection

In this lab, both containers ran on your laptop. In production, the preprocessor would run in the warehouse datacenter and the inference API would run in Congo's main datacenter.

**How would the architecture and your `docker run` commands differ if these containers were actually running in separate datacenters?**

Consider:
- How would the preprocessor find the inference API?
- What about the shared volumes?
- What new challenges would arise?


## Your Reflection Below

The prepocessor finds the inference API using host.docker.internal which works locally. But if it were to be in a seperate datacenter you would need to use a real public URL for the inference.

For shared volumes mounts only work on the same machine. To go across various datacenters you would have to use network storage.

Some challanges that would arise would be network latency between datacenters, authentication & security for the API, handling network failurs and higher cost of sending large image files over the internet. 