import { motion } from "framer-motion";

const AuthLayout = ({ title, children }) => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-600">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="backdrop-blur-xl bg-white/20 p-8 rounded-2xl shadow-2xl w-[380px] text-white"
      >
        <h2 className="text-3xl font-bold mb-6 text-center">{title}</h2>
        {children}
      </motion.div>
    </div>
  );
};

export default AuthLayout;
