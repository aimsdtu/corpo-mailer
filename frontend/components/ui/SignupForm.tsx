"use client";

import * as React from "react";
import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { BarChart, Code, Eye, EyeOff, User } from "lucide-react";
import { useAuth } from "@/context/AuthContext";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardContent, CardFooter } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

const Logo: React.FC = () => (
  <div className="w-10 h-10 bg-black text-white rounded-lg flex items-center justify-center font-bold text-xl tracking-tighter">
    CM
  </div>
);

const SignupForm: React.FC = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [firstName, setFirstName] = useState("");
  const { login } = useAuth();
  const router = useRouter();

  const handleSignup = (e: React.FormEvent) => {
    e.preventDefault();
    const username = firstName.toLowerCase() || "user";
    login(username, "user");
    router.push("/dashboard");
  };

  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="w-full max-w-md">
        <Card className="border-none shadow-lg pb-0">
          <CardHeader className="flex flex-col items-center space-y-1.5 pb-4 pt-6">
            <Logo />
            <div className="space-y-0.5 flex flex-col items-center">
              <h2 className="text-2xl font-semibold text-foreground">
                Create an account
              </h2>
              <p className="text-muted-foreground">
                Welcome! Create an account to get started.
              </p>
            </div>
          </CardHeader>

          <CardContent className="space-y-6 px-8">
            <form onSubmit={handleSignup} className="space-y-6">
              {/* Role */}
              <div className="space-y-2">
                <Label htmlFor="role">Role</Label>
                <Select defaultValue="manager">
                  <SelectTrigger
                    id="role"
                    className="[&>span]:flex [&>span]:items-center [&>span]:gap-2 [&>span_svg]:shrink-0"
                  >
                    <SelectValue placeholder="Select role" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="designer">
                      <User size={16} aria-hidden="true" />
                      <span className="truncate">SDR</span>
                    </SelectItem>
                    <SelectItem value="developer">
                      <Code size={16} aria-hidden="true" />
                      <span className="truncate">Developer</span>
                    </SelectItem>
                    <SelectItem value="manager">
                      <BarChart size={16} aria-hidden="true" />
                      <span className="truncate">Campaign Manager</span>
                    </SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* Name */}
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="firstName">First name</Label>
                  <Input
                    id="firstName"
                    value={firstName}
                    onChange={(e) => setFirstName(e.target.value)}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="lastName">Last name</Label>
                  <Input id="lastName" />
                </div>
              </div>

              {/* Username */}
              <div className="space-y-2">
                <Label htmlFor="username">Username</Label>
                <Input id="username" />
              </div>

              {/* Email */}
              <div className="space-y-2">
                <Label htmlFor="email">Email address</Label>
                <Input id="email" type="email" />
              </div>

              {/* Password */}
              <div className="space-y-2">
                <Label htmlFor="password">Password</Label>
                <div className="relative">
                  <Input
                    id="password"
                    type={showPassword ? "text" : "password"}
                    className="pr-10"
                  />
                  <Button
                    type="button"
                    variant="ghost"
                    size="icon"
                    className="absolute right-0 top-0 h-full px-3 text-muted-foreground hover:bg-transparent"
                    onClick={() => setShowPassword((prev) => !prev)}
                    aria-label={showPassword ? "Hide password" : "Show password"}
                  >
                    {showPassword ? (
                      <EyeOff className="h-4 w-4" />
                    ) : (
                      <Eye className="h-4 w-4" />
                    )}
                  </Button>
                </div>
              </div>

              {/* Terms */}
              <div className="flex items-center space-x-2">
                <Checkbox id="terms" required />
                <label
                  htmlFor="terms"
                  className="text-sm text-muted-foreground"
                >
                  I agree to the{" "}
                  <a href="#" className="text-primary hover:underline">
                    Terms
                  </a>{" "}
                  and{" "}
                  <a href="#" className="text-primary hover:underline">
                    Conditions
                  </a>
                </label>
              </div>

              <Button
                type="submit"
                className="w-full bg-primary text-primary-foreground"
              >
                Create free account
              </Button>
            </form>
          </CardContent>

          <CardFooter className="flex justify-center border-t !py-4">
            <p className="text-center text-sm text-muted-foreground">
              Already have an account?{" "}
              <Link href="/login" className="text-primary hover:underline">
                Sign in
              </Link>
            </p>
          </CardFooter>
        </Card>
      </div>
    </div>
  );
};

export default SignupForm;
