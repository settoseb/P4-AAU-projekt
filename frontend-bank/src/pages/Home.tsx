import { useEffect, useState } from "react";
import { Bar, BarChart, CartesianGrid, XAxis, YAxis, Tooltip } from "recharts";
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";
import { Header } from "@/components/header";

export default function Frontpage() {
    const [saldoHistory, setSaldoHistory] = useState<{ date: string; saldo: number; }[]>([]);

    useEffect(() => {
        fetch(`${import.meta.env.VITE_backend_url}/transaction/transactions`, {
            headers: {
                "Authorization": `Bearer ${localStorage.getItem('token')}`
            }
        })
            .then((response) => response.json())
            .then((data) => {
                const groupedByDate = data.reduce((acc: { [key: string]: number }, transaction: {
                    created_at: string;
                    balance_after: number;
                }) => {
                    const date = transaction.created_at.split('T')[0];
                    acc[date] = transaction.balance_after;
                    return acc;
                }, {});

                const historyData = Object.entries(groupedByDate).map(([date, saldo]) => ({
                    date,
                    saldo
                }));

                // Sort by date
                historyData.sort((a, b) => a.date.localeCompare(b.date));

                setSaldoHistory(historyData);
            })
            .catch((error) => console.error("Error fetching transactions:", error));
    }, []);

    return (
        <>
            <Header />
            <main className="container mx-auto py-6 px-4">
                <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl lg:text-6xl mb-6">
                    Secure banking
                </h1>

                <Card className="mt-6 max-w-3xl mx-auto">
                    <CardHeader>
                        <CardTitle>Saldo Udvikling</CardTitle>
                        <CardDescription>Din saldo historik</CardDescription>
                    </CardHeader>
                    <CardContent >
                        <div style={{ display: "flex", justifyContent: "center", alignItems: "center" }}>
                            <BarChart width={600} height={300} data={saldoHistory}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis
                                    dataKey="date"
                                    tickFormatter={(value) => value.substring(5)}
                                />
                                <YAxis
                                    tickFormatter={(value) => `${value}`}
                                    label={{ value: "DKK", angle: -90, position: "insideLeft" }}
                                />
                                <Tooltip formatter={(value) => `${value}`} />
                                <Bar dataKey="saldo" fill="#82ca9d" barSize={30} />
                            </BarChart>
                        </div>
                    </CardContent>
                </Card>
            </main>
        </>
    );
}