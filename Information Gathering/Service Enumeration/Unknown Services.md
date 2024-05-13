# Identifying unknown services

## Questions to ask yourself
  *  What port is the service running on?
      *  Could that be an indicator of what the service is?
  *  Does the service provide any sort of banner on connection?
  *  Does the service respond to HTTP requests?
  *  How does the service respond to garbage input?

## Things to remember
  *  An unknown service may be referenced within the information of a known service
      *  Research words of interest gathered from known services

## Useful tools
  *  [`netcat`](http://www.stearns.org/nc/) for banner grabbing
  *  [`curl`](https://curl.se/) for HTTP header grabbing

## Banner grab  
  *  A banner grab is the most basic form of service identification
      *  Banner grab results not making any sense? **GTS**

```
nc -nv 10.0.0.1 9999
```

## HTTP grab
  *  No banner on connect? The service may be waiting for an HTTP request
      *  **ALWAYS** try pointing your browser or `curl` at any unknown service

```
curl 'http://10.0.0.1:9999'
```

## Research port numbers
  *  The port number itself may give away information about the running service
      *  [SpeedGuide](http://www.speedguide.net) is a great resource for port numbers and their common uses
      *  **This is obviously not reliable**, but can be a good place to start
