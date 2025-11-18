import { Link, useNavigate } from "react-router-dom";
import { PiggyBank, Home, User, LogIn, LogOut, ArrowRightLeft } from "lucide-react";

export function Header() {
  const isAuthenticated = !!localStorage.getItem('token');
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="mx-auto flex h-14 max-w-7xl items-center px-4">
        <nav className="flex flex-1 items-center justify-between">
          <Link to="/" className="flex items-center gap-2 font-semibold">
            <PiggyBank className="h-5 w-5" />
            <span className="hidden sm:inline-block">Bank App</span>
          </Link>

          <div className="flex items-center gap-4">
            <Link
              to="/"
              className="flex items-center gap-2 rounded-md px-3 py-2 text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground"
            >
              <Home className="h-4 w-4" />
              <span className="hidden sm:inline-block">Home</span>
            </Link>

            {isAuthenticated && (
              <>
                <Link
                  to="/about"
                  className="flex items-center gap-2 rounded-md px-3 py-2 text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground"
                >
                  <User className="h-4 w-4" />
                  <span className="hidden sm:inline-block">Account</span>
                </Link>

                <Link
                  to="/transaction"
                  className="flex items-center gap-2 rounded-md px-3 py-2 text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground"
                >
                  <ArrowRightLeft className="h-4 w-4" />
                  <span className="hidden sm:inline-block">Transaction</span>
                </Link>
              </>
            )}

            {isAuthenticated ? (
              <button
                onClick={handleLogout}
                className="flex items-center gap-2 rounded-md bg-destructive px-3 py-2 text-sm font-medium text-destructive-foreground transition-all hover:bg-destructive/90 hover:scale-105 cursor-pointer active:scale-95"
              >
                <LogOut className="h-4 w-4 text-white" />
                <span className="text-white">Logout</span>
              </button>
            ) : (
              <Link
                to="/login"
                className="flex items-center gap-2 rounded-md bg-primary px-3 py-2 text-sm font-medium text-primary-foreground transition-all hover:bg-primary/90 hover:scale-105 cursor-pointer active:scale-95"
              >
                <LogIn className="h-4 w-4" />
                <span>Login</span>
              </Link>
            )}
          </div>
        </nav>
      </div>
    </header>
  );
}