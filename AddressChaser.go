package main

import (
	"fmt"

	"github.com/phantasma-io/phantasma-go-admin-tools/pkg/analysis"
	"github.com/phantasma-io/phantasma-go/pkg/rpc"
)

//var clients []rpc.PhantasmaRPC
var client rpc.PhantasmaRPC


func main() {
	
	
		//clients = rpc.NewRPCSetMainnet()
		//clients := clients[:2]
		
		clients := []rpc.PhantasmaRPC{
			rpc.NewRPC("https://pharpc1.phantasma.info/rpc"),
			rpc.NewRPC("https://pharpc2.phantasma.info/rpc"),
		}
		//save block height
	
		addresses := analysis.GetAllKnownAddresses(clients,"", true);
	
	
	
		for _, r := range addresses {
			fmt.Printf("%s,", r)
		}


	}