import {
  InputOTP,
  InputOTPGroup,
  InputOTPSeparator,
  InputOTPSlot,
} from "@/components/ui/input-otp"
import { useState } from "react"

import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom"
import { Button } from "@/components/ui/button"
import { REGEXP_ONLY_DIGITS } from "input-otp"


export function MFA({ email }: { email: string }) {
  const navigate = useNavigate()
  const [otp, setOtp] = useState("")
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
   

    try {
      const response = await fetch(
        `${import.meta.env.VITE_backend_url}/auth/verify?verification_code=${otp}&email=${encodeURIComponent(
          email
        )}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
        }
      )

      if (!response.ok) {
        throw new Error("Wrong MFA code")
      }

      const data = await response.json()
      localStorage.setItem("token", data.access_token)
      
      navigate("/")
    } catch (err) {
      setError("Invalid email or password")
    }
  }

    return (
        <div className="flex flex-col items-center my-10"> 
      <p className="mb-4 text-center">
        Please enter your multifactor authentication code sent to your <b>email</b> below
      </p>
          <form onSubmit={handleSubmit}>
            <InputOTP 
            maxLength={6}
            pattern={REGEXP_ONLY_DIGITS}
            onChange={(otp) => setOtp(otp)}
            >
              <InputOTPGroup>
                <InputOTPSlot index={0} />
                <InputOTPSlot index={1} />
                <InputOTPSlot index={2} />
              </InputOTPGroup>
              <InputOTPSeparator />
              <InputOTPGroup>
                <InputOTPSlot index={3} />
                <InputOTPSlot index={4} />
                <InputOTPSlot index={5} />
              </InputOTPGroup>
            </InputOTP>
            <Button className="mt-4" type="submit">Submit</Button>
          </form>
      </div>
    );
}