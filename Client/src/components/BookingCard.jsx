import React, { useState } from "react";
import { Calendar } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogClose,
} from "@/components/ui/dialog";
import ReportModal from "@/components/ReportModal";

const BookingCard = ({ booking }) => {
  const [isDetailsOpen, setIsDetailsOpen] = useState(false);
  const [isReportModalOpen, setIsReportModalOpen] = useState(false);
  const userRole = sessionStorage.getItem("role");

  const toggleDetailsModal = () => setIsDetailsOpen((prev) => !prev);
  const toggleReportModal = () => setIsReportModalOpen((prev) => !prev);

  const getStatusBadgeColor = (status) => {
    switch (status) {
      case "Pending":
        return "bg-yellow-600 text-yellow-100";
      case "Accepted":
        return "bg-green-600 text-green-100";
      case "Rejected":
        return "bg-red-600 text-red-100";
      case "Completed":
        return "bg-blue-600 text-blue-100";
      default:
        return "bg-gray-600 text-gray-100";
    }
  };

  const handleBookingStatus = (newStatus) => {
    console.log(`Changing status to: ${newStatus}`);
    // Add status update logic here
  };

  return (
    <>
      {/* Booking Card */}
      <Card className="bg-gray-900 border-gray-800 rounded-lg shadow-md hover:shadow-lg transition-shadow max-w-md mx-auto">
        <CardContent className="pl-4 pr-6 py-4">
          <div className="flex flex-col gap-4">
            <div className="flex justify-between items-start mb-4">
              <h4 className="text-lg font-semibold text-gray-100">
                {booking.title}
              </h4>
              <Badge
                className={`${getStatusBadgeColor(
                  booking.status
                )} px-2 py-1 rounded`}
              >
                {booking.status}
              </Badge>
            </div>
            <div className="flex justify-between items-center">
              <div className="flex items-center gap-2">
                <Calendar className="h-4 w-4 text-gray-400" />
                <span className="text-sm text-gray-400">
                  {new Date(booking.request_date).toLocaleDateString()} -{" "}
                  {new Date(booking.completion_date).toLocaleDateString()}
                </span>
              </div>
              <Button
                variant="outline"
                className="border-gray-700 hover:bg-gray-800"
                onClick={toggleDetailsModal}
              >
                View Details
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Details Modal */}
      <Dialog open={isDetailsOpen} onOpenChange={toggleDetailsModal}>
        <DialogContent className="bg-gray-900 border border-gray-800 shadow-lg rounded-lg" aria-describedby="">
          <DialogHeader>
            <DialogTitle className="text-lg font-bold text-white">
              Booking Details
            </DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <p className="text-sm text-gray-400 mb-1">Title</p>
              <p className="text-base text-gray-100">{booking.title}</p>
            </div>
            <div>
              <p className="text-sm text-gray-400 mb-1">Status</p>
              <p className="text-base text-gray-100">{booking.status}</p>
            </div>
            <div>
              <p className="text-sm text-gray-400 mb-1">
                {userRole === "Artisan" ? "Client Name" : "Artisan Name"}
              </p>
              <p className="text-base text-gray-100">
                {userRole === "Artisan"
                  ? booking.client_name
                  : booking.artisan_name}
              </p>
            </div>
            <div>
              <p className="text-sm text-gray-400 mb-1">Details</p>
              <p className="text-base text-gray-100">{booking.details}</p>
            </div>
            <div>
              <p className="text-sm text-gray-400 mb-1">Submission Date</p>
              <p className="text-base text-gray-100">
                {new Date(booking.request_date).toLocaleDateString()}
              </p>
            </div>
            <div>
              <p className="text-sm text-gray-400 mb-1">Completion Date</p>
              <p className="text-base text-gray-100">
                {new Date(booking.completion_date).toLocaleDateString()}
              </p>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="mt-6 flex flex-col space-y-4">
            {userRole === "Artisan" && booking.status === "Pending" && (
              <div className="flex gap-4">
                <Button
                  onClick={() => handleBookingStatus("Accepted")}
                  className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg"
                >
                  Accept
                </Button>
                <Button
                  onClick={() => handleBookingStatus("Rejected")}
                  className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg"
                >
                  Reject
                </Button>
              </div>
            )}
            {userRole === "Artisan" && booking.status === "Accepted" && (
              <Button
                onClick={() => handleBookingStatus("Completed")}
                className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg"
              >
                Complete
              </Button>
            )}
            {userRole === "Client" && (
              <>
                <Button
                  onClick={toggleReportModal}
                  className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg"
                >
                  Report Issue
                </Button>
              </>
            )}
            <DialogClose asChild>
              <Button className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg">
                Close
              </Button>
            </DialogClose>
          </div>
        </DialogContent>
      </Dialog>

      {/* Report Modal */}
      <ReportModal
        booking={booking}
        isOpen={isReportModalOpen}
        onClose={toggleReportModal}
      />
    </>
  );
};

export default BookingCard;
