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
import { SignupForm } from "@/components/signup-form"

export default function Signup() {
    return (
        <>
            <Header />
            <div className="flex min-h-[calc(100vh-73px)] w-full items-center justify-center p-6 md:p-10">
                <div className="w-full max-w-sm">
                    <SignupForm />
                </div>
            </div>
        </>
    )
}