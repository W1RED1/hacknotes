package main

import (
        "os"
        "fmt"
        "net"
        "sync"
        "time"
        "strconv"
)

var wg sync.WaitGroup

func probe(target string, port int, timeout int) {
        addr := target + ":" + strconv.Itoa(port)
        conn, err := net.DialTimeout("tcp", addr, time.Duration(timeout)*time.Second)
        if err != nil {
                return
        }

        defer conn.Close()
        fmt.Printf("Port %d: open\n", port)
        return
}

func scan(ports chan int, target string, timeout int, done chan bool) {
        defer wg.Done()
        for {
                select {
                case <- done:
                        return
                case port := <- ports:
                        probe(target, port, timeout)
                }
        }
}


func main() {
        if len(os.Args) != 6 {
                fmt.Println("usage: ./prog [TARGET] [START PORT] [STOP PORT] [TIMEOUT (seconds)] [THREAD COUNT]")
                os.Exit(0)
        }

        // store arguments
        target     := os.Args[1]
        start, _   := strconv.Atoi(os.Args[2])
        stop, _    := strconv.Atoi(os.Args[3])
        timeout, _ := strconv.Atoi(os.Args[4])
        threads, _ := strconv.Atoi(os.Args[5])

        fmt.Printf("Initiating scan against target %s...\n", target)

        clock := time.Now()
        ports := make(chan int)
        done := make(chan bool)

        // spawn workers
        for i := 1; i <= threads; i++ {
                wg.Add(1)
                go scan(ports, target, timeout, done)
        }

        // send jobs to workers until exhausted
        for i := start; i <= stop; i++ {
                ports <- i
        }

        // collect workers
        close(ports)
        for i := 1; i <= threads; i++ {
                done <- true
        }

        wg.Wait()
        duration := time.Since(clock)
        fmt.Printf("\nTime elapsed: %f seconds\n", duration.Seconds())
}
