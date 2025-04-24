package main

import (
	"fmt"

	"github.com/phantasma-io/phantasma-go/pkg/rpc"
	"github.com/phantasma-io/phantasma-go/pkg/rpc/response"
)

var netSelected string
var client rpc.PhantasmaRPC
var chainTokens []response.TokenResult

// AddressChaser is a struct that holds the address and the RPC client
type AddressChaser struct {
	Address string
	client  rpc.PhantasmaRPC
}

func printTokens() {
	for _, t := range chainTokens {
		fmt.Println(t.Symbol, "flags:", t.Flags)
	}
}


func main() {

	client = rpc.NewRPCMainnet()
	chainTokens, _ = client.GetTokens(false)
	fmt.Println("Received information about", len(chainTokens), netSelected, "tokens")

	printTokens()
	// t := getChainToken("SOUL")
	// fmt.Println(t.Symbol, "fungible:", t.IsFungible(), "fuel:", t.IsFuel(), "stakable:", t.IsStakable(), "burnable:", t.IsBurnable(), "transferable:", t.IsTransferable())
	// t = getChainToken("CROWN")
	// fmt.Println(t.Symbol, "fungible:", t.IsFungible(), "fuel:", t.IsFuel(), "stakable:", t.IsStakable(), "burnable:", t.IsBurnable(), "transferable:", t.IsTransferable())
	// t = getChainToken("KCAL")
	// fmt.Println(t.Symbol, "fungible:", t.IsFungible(), "fuel:", t.IsFuel(), "stakable:", t.IsStakable(), "burnable:", t.IsBurnable(), "transferable:", t.IsTransferable())
}
