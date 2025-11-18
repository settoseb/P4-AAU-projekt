import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Separator } from "@/components/ui/separator"
import { Mail, User, Shield } from "lucide-react"

export function AboutCard() {
  const [user, setUser] = useState<{ name: string; email: string; balance: float } | null>(null);

  useEffect(() => {
    const fetchUserData = async () => {
      const response = await fetch(`${import.meta.env.VITE_backend_url}/users/me`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        setUser(data);
      }
    };

    fetchUserData();
  }, []);

  return (
    <div className="container mx-auto py-6 px-4">
      <Card className="max-w-2xl mx-auto border-t-4 border-t-primary shadow-sm">
        <CardHeader className="pb-2">
          <div className="flex items-center gap-4">
            <div>
              <CardTitle className="text-xl font-semibold">Account Information</CardTitle>
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid gap-4">
            <div className="flex gap-3 p-3 rounded-lg bg-muted/50">
              <User className="h-5 w-5 text-muted-foreground" />
              <div>
                <p className="text-sm text-muted-foreground">Full Name</p>
                <p className="font-medium">{user ? user.name : 'Loading...'}</p>
              </div>
            </div>

            <div className="flex gap-3 p-3 rounded-lg bg-muted/50">
              <Mail className="h-5 w-5 text-muted-foreground" />
              <div>
                <p className="text-sm text-muted-foreground">Email Address</p>
                <p className="font-medium text-left">{user ? user.email : 'Loading...'}</p>
              </div>
            </div>


            <div className="flex gap-3 p-3 rounded-lg bg-muted/50">
              <Mail className="h-5 w-5 text-muted-foreground" />
              <div>
                <p className="text-sm text-muted-foreground">Balance</p>
                <p className="font-medium">{user ? user.balance : 'Loading...'}</p>
              </div>
            </div>
          </div>



          <Separator />

          <div className="flex items-center justify-between text-sm">
            <div className="flex items-center gap-1 text-muted-foreground">
              <Shield className="h-4 w-4" />
              <span>Secure account information</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
