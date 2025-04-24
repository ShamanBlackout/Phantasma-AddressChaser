package addressmapper

type Address struct {
	origin               string
	token                string
	totalSent            int64
	totalReceived        int64
	sentTransactions     []string
	receivedTransactions []string
}

// Change this to go through the sent transactions and if its a sent transaction, add the amount to the total sent and if its a received transaction, add the amount to the total received
func (a *Address) AddTransaction(transactionID string, amount int64, isSent bool) {
	if isSent {
		a.totalSent += amount
		a.sentTransactions = append(a.sentTransactions, transactionID)
	} else {
		a.totalReceived += amount
		a.receivedTransactions = append(a.receivedTransactions, transactionID)
	}
}

// calcTotalReceived calculates the total amount received by all addresses to the origin address
func calcTotalReceived(addresses []Address) int64 {
	var total int64
	for _, address := range addresses {
		total += address.totalReceived
	}
	return total
}

// calcTotalSent calculates the total amount sent to all addresses from the origin address
func calcTotalSent(addresses []Address) int64 {
	var total int64
	for _, address := range addresses {
		total += address.totalSent
	}
	return total
}
