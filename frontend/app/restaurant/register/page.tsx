import AuthForm from "../../../components/AuthForm";

export default function RestaurantRegisterPage() {
  return (
    <div className="py-12 flex justify-center items-center px-4 min-h-[calc(100vh-4rem)]">
      <AuthForm type="register" role="restaurant" />
    </div>
  );
}
