"use client";

import { useState } from "react";

export default function Home() {
  const [city, setCity] = useState("Madinah");
  const [days, setDays] = useState(3);
  const [budget, setBudget] = useState(2500);

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState("");

  const createTrip = async () => {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/trips/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            user_request: `${city}, ${days} days, budget ${budget} SAR`,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "حدث خطأ في إنشاء الرحلة"
        );
      }

      setResult(data);
    } catch (err: any) {
      setError(
        err.message || "تعذر الاتصال بالخادم"
      );
    } finally {
      setLoading(false);
    }
  };

  const trip = result?.data;

  /*
   * ScheduleAgent عندك يرجع:
   *
   * {
   *   "Day 1": [...],
   *   "Day 2": [...],
   *   "Day 3": [...]
   * }
   *
   * لذلك نتعامل معه كـ Object وليس Array.
   */
  const schedule =
    trip?.schedule &&
    typeof trip.schedule === "object"
      ? trip.schedule
      : {};

  /*
   * الفندق المختار من ScheduleAgent
   */
  const hotel = trip?.hotel || null;

  /*
   * الأماكن والمطاعم الأصلية القادمة من الـBackend
   */
  const places = Array.isArray(trip?.places)
    ? trip.places
    : [];

  const restaurants = Array.isArray(
    trip?.restaurants
  )
    ? trip.restaurants
    : [];

  /*
   * حساب سعر الفندق
   */
  const hotelPrice =
    typeof hotel?.price_per_night === "number"
      ? hotel.price_per_night
      : typeof hotel?.price === "number"
      ? hotel.price
      : typeof hotel?.nightly_price === "number"
      ? hotel.nightly_price
      : 0;

  const hotelTotal =
    hotelPrice > 0
      ? hotelPrice * days
      : 0;

  /*
   * حساب عدد الأيام الفعلية
   */
  const totalDays =
    Number(trip?.days) || days;

  return (
    <main className="min-h-screen bg-slate-50 text-gray-900">

      {/* =====================================================
          HEADER
      ===================================================== */}

      <header className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-6 py-5">

          <h1 className="text-2xl font-bold text-emerald-700">
            Madinah AI Planner
          </h1>

          <p className="text-sm text-gray-500 mt-1">
            خطط رحلتك إلى المدينة المنورة باستخدام الذكاء الاصطناعي
          </p>

        </div>
      </header>


      {/* =====================================================
          HERO + INPUT
      ===================================================== */}

      <section className="max-w-7xl mx-auto px-6 pt-14">

        <div className="max-w-3xl">

          <p className="text-emerald-700 font-semibold mb-3">
            AI Travel Planner
          </p>

          <h2 className="text-5xl font-bold leading-tight">
            خطط رحلتك إلى{" "}
            <span className="text-emerald-700">
              المدينة المنورة
            </span>{" "}
            بذكاء.
          </h2>

          <p className="text-gray-600 text-lg mt-6 leading-8">
            أدخل وجهتك ومدة الرحلة والميزانية،
            وسيقوم الذكاء الاصطناعي ببناء خطة
            متكاملة تناسب رحلتك.
          </p>

        </div>


        {/* INPUT CARD */}

        <div className="bg-white rounded-3xl border shadow-sm p-8 mt-10">

          <div className="grid md:grid-cols-3 gap-6">

            {/* المدينة */}

            <div>

              <label className="block text-sm font-semibold mb-2">
                الوجهة
              </label>

              <input
                value={city}
                onChange={(e) =>
                  setCity(e.target.value)
                }
                className="w-full border rounded-xl px-4 py-3 outline-none focus:ring-2 focus:ring-emerald-200"
                placeholder="Madinah"
              />

            </div>


            {/* عدد الأيام */}

            <div>

              <label className="block text-sm font-semibold mb-2">
                عدد الأيام
              </label>

              <input
                type="number"
                min="1"
                value={days}
                onChange={(e) =>
                  setDays(Number(e.target.value))
                }
                className="w-full border rounded-xl px-4 py-3 outline-none focus:ring-2 focus:ring-emerald-200"
              />

            </div>


            {/* الميزانية */}

            <div>

              <label className="block text-sm font-semibold mb-2">
                الميزانية
              </label>

              <input
                type="number"
                min="1"
                value={budget}
                onChange={(e) =>
                  setBudget(Number(e.target.value))
                }
                className="w-full border rounded-xl px-4 py-3 outline-none focus:ring-2 focus:ring-emerald-200"
                placeholder="2500"
              />

            </div>

          </div>


          {/* BUTTON */}

          <button
            onClick={createTrip}
            disabled={loading}
            className="w-full mt-8 bg-emerald-700 hover:bg-emerald-800 disabled:bg-gray-400 text-white font-semibold py-4 rounded-xl transition"
          >

            {loading
              ? "⏳ جاري إعداد رحلتك..."
              : "✨ أنشئ رحلتي بالذكاء الاصطناعي"}

          </button>

        </div>

      </section>


      {/* =====================================================
          ERROR
      ===================================================== */}

      {error && (

        <section className="max-w-7xl mx-auto px-6 mt-6">

          <div className="bg-red-50 border border-red-200 text-red-600 rounded-2xl p-5">

            {error}

          </div>

        </section>

      )}


      {/* =====================================================
          TRIP RESULT
      ===================================================== */}

      {trip && (

        <section className="max-w-7xl mx-auto px-6 py-12">


          {/* =================================================
              TRIP HEADER
          ================================================= */}

          <div className="bg-emerald-700 text-white rounded-3xl p-8 mb-8">

            <p className="text-emerald-100 text-sm">
              خطتك السياحية
            </p>

            <h2 className="text-3xl font-bold mt-2">
              رحلتك إلى {trip.city}
            </h2>

            <p className="text-emerald-100 mt-2">
              {totalDays} أيام مصممة لك بالذكاء الاصطناعي
            </p>

          </div>


          {/* =================================================
              HOTEL
          ================================================= */}

          <div className="mb-10">

            <h3 className="text-2xl font-bold mb-5">
              🏨 الفندق المقترح
            </h3>


            {hotel ? (

              <div className="bg-white border rounded-3xl p-7 shadow-sm">

                <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-5">


                  {/* معلومات الفندق */}

                  <div>

                    <h4 className="text-xl font-bold">
                      {hotel.name || "الفندق المقترح"}
                    </h4>


                    {hotel.rating && (

                      <p className="text-yellow-600 mt-2">
                        ⭐ {hotel.rating}
                      </p>

                    )}


                    {hotel.address && (

                      <p className="text-gray-500 mt-2">
                        📍 {hotel.address}
                      </p>

                    )}

                  </div>


                  {/* السعر */}

                  <div className="text-left md:text-right">

                    {hotelPrice > 0 && (

                      <>
                        <p className="text-gray-500 text-sm">
                          السعر لكل ليلة
                        </p>

                        <p className="text-2xl font-bold text-emerald-700">
                          {hotelPrice} SAR
                        </p>

                        <p className="text-sm text-gray-500 mt-1">
                          إجمالي الإقامة:{" "}
                          {hotelTotal} SAR
                        </p>
                      </>

                    )}

                  </div>

                </div>

              </div>

            ) : (

              <div className="bg-white border rounded-3xl p-7 text-gray-500">
                لم يتم العثور على فندق في هذه النتيجة.
              </div>

            )}

          </div>


          {/* =================================================
              DAILY ITINERARY
          ================================================= */}

          <div className="mb-10">

            <div className="flex items-center justify-between mb-5">

              <h3 className="text-2xl font-bold">
                🗓️ جدول الرحلة المقترح
              </h3>

              <span className="text-sm text-gray-500">
                {totalDays} أيام
              </span>

            </div>


            {/* =================================================
                DAYS
            ================================================= */}

            <div className="space-y-6">

              {Array.from(
                { length: totalDays },
                (_, index) => {

                  const dayNumber = index + 1;

                  /*
                   * ScheduleAgent:
                   *
                   * "Day 1"
                   * "Day 2"
                   * "Day 3"
                   */

                  const daySchedule =
                    schedule[
                      `Day ${dayNumber}`
                    ] || [];


                  return (

                    <div
                      key={dayNumber}
                      className="bg-white border rounded-3xl shadow-sm overflow-hidden"
                    >

                      {/* =====================================
                          DAY HEADER
                      ===================================== */}

                      <div className="bg-emerald-700 text-white px-6 py-5">

                        <div className="flex items-center justify-between">

                          <div>

                            <h4 className="text-xl font-bold">
                              اليوم {dayNumber}
                            </h4>

                            <p className="text-emerald-100 text-sm mt-1">
                              خطة اليوم المقترحة
                            </p>

                          </div>

                          <div className="text-3xl">
                            {dayNumber === 1
                              ? "🌅"
                              : dayNumber === 2
                              ? "☀️"
                              : "🌇"}
                          </div>

                        </div>

                      </div>


                      {/* =====================================
                          DAY TABLE
                      ===================================== */}

                      <div className="overflow-x-auto">

                        <table className="w-full min-w-[900px]">

                          <thead>

                            <tr className="bg-gray-50 border-b">

                              <th className="text-right p-4 font-semibold">
                                الوقت
                              </th>

                              <th className="text-right p-4 font-semibold">
                                النشاط
                              </th>

                              <th className="text-right p-4 font-semibold">
                                النوع
                              </th>

                              <th className="text-right p-4 font-semibold">
                                التقييم
                              </th>

                              <th className="text-right p-4 font-semibold">
                                السعر
                              </th>

                            </tr>

                          </thead>


                          <tbody>

                            {daySchedule.length > 0 ? (

                              daySchedule.map(
                                (
                                  activity: any,
                                  activityIndex: number
                                ) => (

                                  <tr
                                    key={activityIndex}
                                    className="border-b last:border-b-0 hover:bg-gray-50 transition"
                                  >

                                    {/* الوقت */}

                                    <td className="p-4">

                                      <span className="inline-block bg-emerald-50 text-emerald-700 font-semibold px-3 py-1 rounded-lg text-sm">
                                        {activity.time || "--"}
                                      </span>

                                    </td>


                                    {/* النشاط */}

                                    <td className="p-4">

                                      <div className="font-semibold text-gray-900">

                                        {activity.name ||
                                          "غير محدد"}

                                      </div>


                                      {activity.address && (

                                        <div className="text-sm text-gray-500 mt-1">

                                          📍{" "}
                                          {activity.address}

                                        </div>

                                      )}

                                    </td>


                                    {/* النوع */}

                                    <td className="p-4">

                                      {activity.category ===
                                      "restaurant" ? (

                                        <span className="text-sm">
                                          🍽️ مطعم
                                        </span>

                                      ) : (

                                        <span className="text-sm">
                                          📍 مكان سياحي
                                        </span>

                                      )}

                                    </td>


                                    {/* التقييم */}

                                    <td className="p-4">

                                      {activity.rating ? (

                                        <span className="text-yellow-600">
                                          ⭐{" "}
                                          {activity.rating}
                                        </span>

                                      ) : (

                                        <span className="text-gray-400">
                                          --
                                        </span>

                                      )}

                                    </td>


                                    {/* السعر */}

                                    <td className="p-4">

                                      {activity.price ? (

                                        <span className="font-semibold text-emerald-700">
                                          {activity.price}
                                        </span>

                                      ) : activity.category ===
                                        "restaurant" ? (

                                        <span className="text-gray-400">
                                          غير متوفر
                                        </span>

                                      ) : (

                                        <span className="text-gray-500">
                                          مجاني
                                        </span>

                                      )}

                                    </td>

                                  </tr>

                                )
                              )

                            ) : (

                              <tr>

                                <td
                                  colSpan={5}
                                  className="p-10 text-center text-gray-400"
                                >

                                  لا توجد أنشطة مقترحة
                                  لهذا اليوم.

                                </td>

                              </tr>

                            )}

                          </tbody>

                        </table>

                      </div>

                    </div>

                  );

                }
              )}

            </div>

          </div>


          {/* =================================================
              AVAILABLE PLACES
              يظهر فقط إذا لم يكن هناك Schedule
          ================================================= */}

          {places.length > 0 &&
            Object.keys(schedule).length === 0 && (

              <div className="mb-10">

                <div className="bg-amber-50 border border-amber-200 rounded-2xl p-5">

                  <p className="font-semibold text-amber-800">

                    💡 تم العثور على أماكن سياحية،
                    لكن جدول الرحلة اليومي لم يتم توليده بعد.

                  </p>

                  <p className="text-sm text-amber-700 mt-2">

                    الأماكن المتاحة: {places.length}

                  </p>

                </div>

              </div>

            )}


          {/* =================================================
              RESTAURANTS
          ================================================= */}

          {restaurants.length > 0 && (

            <div className="mb-10">

              <h3 className="text-2xl font-bold mb-5">
                🍽️ المطاعم المتاحة
              </h3>


              <div className="grid md:grid-cols-3 gap-5">

                {restaurants.map(
                  (
                    restaurant: any,
                    index: number
                  ) => (

                    <div
                      key={index}
                      className="bg-white border rounded-2xl p-5"
                    >

                      <h4 className="font-bold">

                        {restaurant.name}

                      </h4>


                      {restaurant.rating && (

                        <p className="text-yellow-600 mt-2">

                          ⭐ {restaurant.rating}

                        </p>

                      )}


                      {restaurant.price && (

                        <p className="text-gray-500 text-sm mt-2">

                          💰 {restaurant.price}

                        </p>

                      )}

                    </div>

                  )
                )}

              </div>

            </div>

          )}


          {/* =================================================
              TOTAL BUDGET
          ================================================= */}

          <div className="bg-gray-900 text-white rounded-3xl p-8">

            <p className="text-gray-400">
              الميزانية المحددة للرحلة
            </p>


            <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-5">

              <div>

                <h3 className="text-4xl font-bold mt-2">

                  {budget.toLocaleString()} SAR

                </h3>

                <p className="text-gray-400 mt-2">

                  الميزانية التي حددتها للرحلة

                </p>

              </div>


              {hotelTotal > 0 && (

                <div className="text-sm text-gray-400">

                  تكلفة الفندق المقدرة:{" "}

                  <span className="text-white font-semibold">

                    {hotelTotal.toLocaleString()} SAR

                  </span>

                </div>

              )}

            </div>

          </div>

        </section>

      )}

    </main>
  );
}