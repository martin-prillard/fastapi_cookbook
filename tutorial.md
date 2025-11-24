Tutorial on API serving & monitoring

Note that we will be using the iris dataset & sklearn for convenience, speed and ease of use - obviously, training is not the main purpose of this course. The iris dataset ask

If you have docker already, launch the following command in this repository. 
Otherwise, download either docker or docker desktop depending on your operating system before doing so.
```bash
docker compose up --build
```
Depending on your connection, it may take a while so do it at the beginning of the class.
If you are unable to get docker running, focus on the questions about the API.

## First part : File analysis

#### Question 1:
What services are being built using this docker compose? Are they all built the same way? 
How are they connected? 

#### Question 2: 
Can you identify a potential security problem if you were to put that in production "as is"?

#### Question 3: 
What happens to the stored metrics if one of the monitoring services fails?

#### Question 4: 
Let's focus on the FastAPI. How many endpoints can you identify? What are they used for? 
What is the difference between GET and POST?
How can you verify that the API is indeed running?

#### Question 5:
Why wouldn't it be a good idea to add the possibility to train using the API?

#### Question 6:
Let's focus on the prometheus.yml file. What is it about?

#### Question 7:
Let's focus on the fastapi_dashboard.json file. What is it about?

## Second part : Hands on
Let's check the 3 UIs that we made available :
A FastAPI swagger at http://localhost:8000/docs
The Prometheus client at http://localhost:9090/
The Grafana dashboard at http://localhost:3000/

#### Question 1:
Launch a few requests using the FastAPI swagger to make some basic predictions.
What is the model used behind those predictions? Would we get an error if
we performed inference for a data point largely out of distribution?

#### Question 2:
In the POST endpoint of the API, add a way to check if a datapoint is largely out of distribution and if it is the case, return a warning in the response content.

#### Question 3:
What is a huge limitation in terms of speed & network throughput in the case a user wants several predictions instead of only one?

#### Question 4:
In Prometheus, where can you check the endpoint to which it is linked?

#### Question 5:
Once you ensured Prometheus is linked to the FastAPI metrics endpoint, 
use the FastAPI swagger to generate a handful of new predictions.
Type your first request in the expression bar :
```
api_requests_total
```
What info does it give us? How can you check that the information is retained 
through time, so that you can follow the evolution of the use of your API?

#### Question 6:
In regard to question 3, how is this indicator kind of rigged?

#### Question 7:
Let's launch a little more complex command :
```
histogram_quantile(0.95, rate(api_request_latency_seconds_bucket[1m]))
```
What are we aiming to achieve by using this command? What is the reason behind the graph 
spiking?

### Question 8:
In Grafana, we don't have access yet to the data stored by Prometheus. Check the Connections/ Data Sources panel. We have to connect them using the button "Add new Data Source". Choose Prometheus and modify the Prometheus server URL to be http://prometheus:9090. Congratulations, they are now linked.

### Question 9:
We will now have to get our dashboard running. Go to the Dashboards panel, click on the "New" button, and choose "Import" to import the fastapi_dashboard.json file. You should now be able to see the dashboards. Modify the filters and edit them so that they look prettier and more readable. You can also design a python script that requests the API randomly and "en masse" to simulate the real usage of your API.

### Question 10:
Create a new grafana dashboard to provide the median and mean latency of your requests 
to the API.

### Question 11:
Consult Grafana documentation to get more familiar with the framework. What could we want to do to react very quickly to a sudden spike in our mean API latency?

### Question 12:
Overall, what is your conclusion on why adding a monitoring system might be important to ensure everything runs smoothly without having to check every system you deployed manually?

### Question 13:
What typical metrics do we want to log?

### Question 14:
How should we modify our system to add CPU usage tracking to our Grafana dashboards? Do it.