import { useEffect, useState } from "react";
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"

import { Header } from "@/components/header"
import { AboutCard } from "@/components/about-card"

export default function About() {
    return (
        <>
            <Header />
            <AboutCard />
        </>
    )
}