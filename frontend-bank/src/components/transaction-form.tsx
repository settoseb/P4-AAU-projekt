import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";
import Swal from 'sweetalert2';
import { Input } from "@/components/ui/input";
import { Table, TableBody, TableCaption, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

export function TransactionForm({
    className,
    ...props
}: React.ComponentProps<"form">) {
    const [ID, setID] = useState("");
    const [amount, setAmount] = useState("");
    const [error, setError] = useState("");
    const [transactions, setTransactions] = useState([]);
    const navigate = useNavigate();

    const fetchTransactions = async () => {
        try {
            const response = await fetch(`${import.meta.env.VITE_backend_url}/transaction/transactions`, {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${localStorage.getItem('token')}`
                },
            });

            if (!response.ok) {
                throw new Error("Failed to fetch transactions");
            }

            const data = await response.json();
            setTransactions(data);
        } catch (err) {
            console.error("Error fetching transactions:", err);
        }
    };

    useEffect(() => {
        fetchTransactions();
    }, []);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");
        const parsedID = parseInt(ID, 10);
        const parsedAmount = parseFloat(amount);
        if (isNaN(parsedID) || isNaN(parsedAmount) || parsedAmount <= 0) {
            setError("Invalid ID or amount");
            return;
        }

        try {
            const response = await fetch(`${import.meta.env.VITE_backend_url}/transaction/transaction`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({ to_id: parsedID, amount: parsedAmount }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || "Transaction failed");
            }

            await Swal.fire({
                title: "Transaction Successful!",
                text: "Transaction was made succesfully",
                icon: "success",
                confirmButtonColor: '#3085d6',
            });

            fetchTransactions();
            navigate("/");
        } catch (err) {
            setError("Invalid Id or amount");
        }
    };

    const formatDate = (dateString: string) => {
        const date = new Date(dateString)
        return new Intl.DateTimeFormat("en-US", {
            year: "numeric",
            month: "short",
            day: "2-digit",
            hour: "2-digit",
            minute: "2-digit",
        }).format(date)
    }

    return (
        <>
            <Card className="max-w-3xl">
                <CardHeader>
                    <CardTitle>Make a transaction</CardTitle>
                    <CardDescription>
                        Enter details below to make a transaction
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <form onSubmit={handleSubmit} className={cn("flex flex-col gap-6", className)} {...props}>
                        <label>
                            Enter the ID of the receiver:
                            <Input
                                type="number"
                                value={ID}
                                onChange={(e: React.ChangeEvent<HTMLInputElement>) => setID(e.target.value)}
                                required
                            />
                        </label>
                        <label>
                            Enter the amount:
                            <Input
                                type="number"
                                value={amount}
                                onChange={(e: React.ChangeEvent<HTMLInputElement>) => setAmount(e.target.value)}
                                required
                            />
                        </label>
                        <Button type="submit" className="w-full">
                            Make transaction
                        </Button>
                    </form>
                </CardContent>
            </Card>

            <Card className="mt-6 max-w-3xl">
                <CardHeader>
                    <CardTitle>💸Your Transactions💸</CardTitle>
                    <CardDescription>A history of your recent transactions</CardDescription>
                </CardHeader>
                <CardContent>
                    {transactions.length === 0 ? (
                        <p>No transactions found</p>
                    ) : (
                        <Table>
                            <TableHeader>
                                <TableRow>
                                    <TableHead>To ID</TableHead>
                                    <TableHead>Amount</TableHead>
                                    <TableHead>Balance After</TableHead>
                                    <TableHead>Date</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {transactions.map((transaction: any) => (
                                    <TableRow key={transaction.created_at}>
                                        <TableCell>{transaction.to_id}</TableCell>
                                        <TableCell>
                                            {transaction.amount}
                                        </TableCell>
                                        <TableCell>{transaction.balance_after}</TableCell>
                                        <TableCell>{formatDate(transaction.created_at)}</TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    )}
                </CardContent>
            </Card>
        </>
    );
}
