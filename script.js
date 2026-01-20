// Плавный скролл по разделам
document.querySelectorAll("[data-scroll-to]").forEach((el) => {
  el.addEventListener("click", () => {
    const target = el.getAttribute("data-scroll-to");
    if (!target) return;
    const section = document.querySelector(target);
    if (section) {
      section.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  });
});

// Эффект при скролле для header
window.addEventListener('scroll', () => {
  const header = document.querySelector('.header');
  if (window.scrollY > 50) {
    header.classList.add('scrolled');
  } else {
    header.classList.remove('scrolled');
  }
});

// Intersection Observer для анимации при прокрутке
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
    }
  });
}, observerOptions);

// Применяем анимацию к карточкам при загрузке
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(card);
  });
});

// Утилиты для работы с датами
function formatDate(date) {
  return date.toISOString().split('T')[0];
}

function getTimeSlots() {
  const slots = [];
  for (let hour = 10; hour <= 20; hour++) {
    slots.push(`${hour.toString().padStart(2, '0')}:00`);
    if (hour < 20) {
      slots.push(`${hour.toString().padStart(2, '0')}:30`);
    }
  }
  return slots;
}

function isTimeSlotAvailable(date, time, bookings) {
  const datetime = `${date}T${time}`;
  return !bookings.some(b => b.datetime === datetime);
}

// Создание календаря с выбором времени
function createCalendarPicker(containerId, inputId) {
  const container = document.getElementById(containerId);
  const input = document.getElementById(inputId);
  if (!container || !input) return;

  let selectedDate = null;
  let selectedTime = null;
  const today = new Date();
  let viewMonth = today.getMonth();
  let viewYear = today.getFullYear();

  // Создаем календарь
  function renderCalendar() {
    const bookings = loadBookings();
    const currentMonth = today.getMonth();
    const currentYear = today.getFullYear();
    
    if (selectedDate) {
      viewMonth = selectedDate.getMonth();
      viewYear = selectedDate.getFullYear();
    }

    const firstDay = new Date(viewYear, viewMonth, 1);
    const lastDay = new Date(viewYear, viewMonth + 1, 0);
    const daysInMonth = lastDay.getDate();
    const startDayOfWeek = firstDay.getDay() === 0 ? 6 : firstDay.getDay() - 1;

    let calendarHTML = `
      <div class="calendar-header">
        <button type="button" class="calendar-nav" data-action="prev">‹</button>
        <span class="calendar-month">${firstDay.toLocaleDateString('ru-RU', { month: 'long', year: 'numeric' })}</span>
        <button type="button" class="calendar-nav" data-action="next">›</button>
      </div>
      <div class="calendar-weekdays">
        <div>Пн</div><div>Вт</div><div>Ср</div><div>Чт</div><div>Пт</div><div>Сб</div><div>Вс</div>
      </div>
      <div class="calendar-days">
    `;

    // Пустые ячейки до первого дня месяца
    for (let i = 0; i < startDayOfWeek; i++) {
      calendarHTML += '<div class="calendar-day calendar-day--empty"></div>';
    }

    // Дни месяца
    for (let day = 1; day <= daysInMonth; day++) {
      const date = new Date(viewYear, viewMonth, day);
      const dateStr = formatDate(date);
      const isPast = date < today && formatDate(date) !== formatDate(today);
      const isSelected = selectedDate && formatDate(selectedDate) === dateStr;
      const classes = ['calendar-day'];
      if (isPast) classes.push('calendar-day--past');
      if (isSelected) classes.push('calendar-day--selected');
      
      calendarHTML += `<div class="${classes.join(' ')}" data-date="${dateStr}">${day}</div>`;
    }

    calendarHTML += '</div></div>';

    // Временные слоты
    if (selectedDate) {
      const timeSlots = getTimeSlots();
      const dateStr = formatDate(selectedDate);
      calendarHTML += `
        <div class="time-slots">
          <h4>Выберите время:</h4>
          <div class="time-slots-grid">
      `;
      
      timeSlots.forEach(time => {
        const isAvailable = isTimeSlotAvailable(dateStr, time, bookings);
        const isSelected = selectedTime === time;
        const classes = ['time-slot'];
        if (!isAvailable) classes.push('time-slot--busy');
        if (isSelected) classes.push('time-slot--selected');
        
        calendarHTML += `<button type="button" class="${classes.join(' ')}" data-time="${time}" ${!isAvailable ? 'disabled' : ''}>${time}</button>`;
      });
      
      calendarHTML += '</div></div>';
    }

    container.innerHTML = calendarHTML;

    // Обработчики событий
    container.querySelectorAll('.calendar-day:not(.calendar-day--past):not(.calendar-day--empty)').forEach(day => {
      day.addEventListener('click', () => {
        selectedDate = new Date(day.dataset.date + 'T00:00:00');
        selectedTime = null;
        renderCalendar();
      });
    });

    container.querySelectorAll('.time-slot:not(.time-slot--busy)').forEach(slot => {
      slot.addEventListener('click', () => {
        selectedTime = slot.dataset.time;
        const datetime = `${formatDate(selectedDate)}T${selectedTime}`;
        input.value = datetime;
        renderCalendar();
        // Закрываем календарь после выбора
        setTimeout(() => {
          container.style.display = 'none';
        }, 300);
      });
    });

    container.querySelectorAll('.calendar-nav').forEach(btn => {
      btn.addEventListener('click', () => {
        if (btn.dataset.action === 'prev') {
          viewMonth--;
          if (viewMonth < 0) {
            viewMonth = 11;
            viewYear--;
          }
        } else {
          viewMonth++;
          if (viewMonth > 11) {
            viewMonth = 0;
            viewYear++;
          }
        }
        selectedDate = new Date(viewYear, viewMonth, selectedDate ? selectedDate.getDate() : 1);
        renderCalendar();
      });
    });
  }

  // Показываем календарь при клике на input
  input.addEventListener('focus', () => {
    container.style.display = 'block';
    renderCalendar();
  });

  // Закрываем при клике вне календаря
  document.addEventListener('click', (e) => {
    if (!container.contains(e.target) && e.target !== input) {
      container.style.display = 'none';
    }
  });
}

// Фильтрация услуг по категориям
const serviceFilters = document.getElementById("service-filters");
const serviceCards = document.querySelectorAll(".service-card");

if (serviceFilters) {
  serviceFilters.addEventListener("click", (e) => {
    const btn = e.target.closest(".chip");
    if (!btn) return;

    const filter = btn.dataset.filter || "all";

    serviceFilters
      .querySelectorAll(".chip")
      .forEach((chip) => chip.classList.remove("chip--active"));
    btn.classList.add("chip--active");

    serviceCards.forEach((card) => {
      const category = card.dataset.category;
      const show = filter === "all" || category === filter;
      card.style.display = show ? "" : "none";
    });
  });
}

// Работа с записями (демо, localStorage)
const STORAGE_KEY = "beauty_studio_bookings_v1";

function loadBookings() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function saveBookings(bookings) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(bookings));
  } catch {
    // ignore
  }
}

function formatDateTime(value) {
  if (!value) return "";
  try {
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return value;

    return date.toLocaleString("ru-RU", {
      day: "2-digit",
      month: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
    });
  } catch {
    return value;
  }
}

function renderBookings() {
  const list = document.getElementById("booking-list");
  const empty = document.getElementById("booking-empty");
  if (!list || !empty) return;

  const bookings = loadBookings().sort(
    (a, b) => new Date(a.datetime) - new Date(b.datetime)
  );

  list.innerHTML = "";

  if (!bookings.length) {
    empty.style.display = "";
    return;
  }

  empty.style.display = "none";

  bookings.forEach((item) => {
    const li = document.createElement("li");
    li.className = "booking-list__item";

    li.innerHTML = `
      <div class="booking-list__main">
        <span class="booking-list__name">${item.name}</span>
        <span class="booking-list__service">${item.service}</span>
        <span class="booking-list__meta">Мастер: ${item.master}</span>
      </div>
      <div class="booking-list__meta">
        <div class="booking-list__time">${formatDateTime(item.datetime)}</div>
        <div>${item.phone}</div>
        ${
          item.comment
            ? `<div style="margin-top:2px;color:rgba(200,200,230,0.8)">${item.comment}</div>`
            : ""
        }
      </div>
    `;

    list.appendChild(li);
  });
}

function handleBookingForm(formId) {
  const form = document.getElementById(formId);
  if (!form) return;

  form.addEventListener("submit", (e) => {
    e.preventDefault();

    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    if (!data.name || !data.phone || !data.datetime) {
      alert("Пожалуйста, заполните обязательные поля.");
      return;
    }

    const booking = {
      id: Date.now(),
      name: data.name.trim(),
      phone: data.phone.trim(),
      service: (data.service || "Услуга не выбрана").toString(),
      master: (data.master || "Без мастера").toString(),
      datetime: data.datetime,
      comment: (data.comment || "").toString().trim(),
    };

    const bookings = loadBookings();
    bookings.push(booking);
    saveBookings(bookings);
    renderBookings();

    form.reset();

    if ("datetime" in form.elements) {
      form.elements.datetime.value = "";
    }

    showNotification("✓ Запись успешно сохранена!", "success");
    
    // Отправка события для аналитики (если подключена)
    if (typeof gtag !== 'undefined') {
      gtag('event', 'booking_created', {
        'event_category': 'engagement',
        'event_label': booking.service
      });
    }
    
    if (typeof ym !== 'undefined') {
      ym(counterId, 'reachGoal', 'booking_created');
    }
  });
}

// Основная форма записи
handleBookingForm("booking-form");

// Быстрая форма
handleBookingForm("quick-booking-form");

renderBookings();

// Инициализация календарей после загрузки DOM
document.addEventListener('DOMContentLoaded', () => {
  createCalendarPicker("quick-calendar", "quick-datetime");
  createCalendarPicker("booking-calendar", "booking-datetime");
});

// Очистка всех записей
const clearBtn = document.getElementById("clear-bookings");
if (clearBtn) {
  clearBtn.addEventListener("click", () => {
    if (!confirm("Очистить все записи? Действие невозможно отменить.")) {
      return;
    }
    saveBookings([]);
    renderBookings();
    // Перерисовываем календари, чтобы обновить занятые слоты
    if (document.getElementById("quick-calendar").style.display === 'block') {
      createCalendarPicker("quick-calendar", "quick-datetime");
    }
    if (document.getElementById("booking-calendar").style.display === 'block') {
      createCalendarPicker("booking-calendar", "booking-datetime");
    }
  });
}

// Улучшенное уведомление о сохранении записи
function showNotification(message, type = 'success') {
  const notification = document.createElement('div');
  notification.className = `notification notification--${type}`;
  notification.textContent = message;
  document.body.appendChild(notification);
  
  setTimeout(() => {
    notification.classList.add('notification--show');
  }, 10);
  
  setTimeout(() => {
    notification.classList.remove('notification--show');
    setTimeout(() => notification.remove(), 300);
  }, 3000);
}

